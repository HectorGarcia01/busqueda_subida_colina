'''Datos para nuestro problema: 
    nodos: A,B,C,D,E,F
    aristas: AB,AC,BD,BE,CF,DE,EF
    A: 3 = nodo inicial
    B: 2
    C: 2
    D: 3
    E: 1
    F: 0 nodo objetivo

'''
import networkx as nx
import matplotlib.pyplot as plt

# Función para crear y dibujar el grafo
def crear_grafo(nodos, aristas, distancias):
    # Creamos el grafo
    grafo = nx.Graph()
    
    # Agregamos los nodos
    grafo.add_nodes_from(nodos)
    
    # Agregamos las aristasy su distancia
    for arista in aristas:
        nodo1, nodo2 = arista[0], arista[1]
        valor_distancia = distancias[nodo1] + distancias[nodo2]
        grafo.add_edge(nodo1, nodo2, weight=valor_distancia)
    
    # Dibujamos el grafo
    posicion_nodos = nx.spring_layout(grafo)
    nx.draw(grafo, pos=posicion_nodos, with_labels=True)

    # Agregamos las etiquetas de las distancias en las aristas
    etiquetas = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, pos=posicion_nodos, edge_labels=etiquetas)

    # Asignamos un nombre a la figura 
    plt.title("Grafo dibujado")

    # Definimos un objeto manager
    manager = plt.get_current_fig_manager()

    # Asignamos un nombre a la ventana
    manager.set_window_title("Grafo creado")

    # Cambiamos la posición de la ventana
    manager.window.setGeometry(0, 30, manager.window.width(), manager.window.height())

    # Retornamos el grafo
    return grafo

# Función heurística
def heuristica(nodo, distancias):
    return distancias[nodo]

# Búsqueda subida de colina
def busqueda_subida_colina(grafo, nodo_inicio, nodo_objetivo, distancias):
    nodo_actual = nodo_inicio
    
    while nodo_actual != nodo_objetivo:
        vecinos = list(grafo.neighbors(nodo_actual))
        mejor_vecino = None
        mejor_puntuacion = float('inf')
        
        for vecino in vecinos:
            puntuacion = heuristica(vecino, distancias)
            if puntuacion < mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_vecino = vecino
        
        if mejor_puntuacion >= heuristica(nodo_actual, distancias):
            return None # No se puede mejorar la solución
        
        nodo_actual = mejor_vecino
    
    return nodo_actual

# Ejemplo de uso
if __name__ == '__main__':
    print("***************************************************************************************************************************************************")
    
    # Pedir al usuario que ingrese el grafo
    nodos = input("Ingrese los nodos del grafo separados por coma 'A,B,C,D,E,F': ").upper().split(",")
    
    # Pedir al usuario que ingrese las aristas
    aristas = input("Ingrese las aristas del grafo separadas por coma y sin espacios 'AB,AC,BD,BE,CF,DE,EF': ").upper().split(",")

    print("***************************************************************************************************************************************************")

    # Se define un diccionario vacío para las distancias heurísticas de cada arista
    distancias = {}

    for nodo in nodos:
        distancia = int(input(f"Ingrese la distancia heurística del nodo {nodo}: "))
        distancias[nodo] = distancia    
    
    # Llamamos la función para crear y dibujar el grafo
    grafo = crear_grafo(nodos, aristas, distancias)

    print("***************************************************************************************************************************************************")    
    
    # Pedir al usuario que ingrese el nodo de inicio
    nodo_inicio = input("Ingrese el nodo de inicio: ").upper()

    # Pedir al usuario que ingrese el nodo objetivo
    nodo_objetivo = input("Ingrese el nodo objetivo: ").upper()
    
    resultado = busqueda_subida_colina(grafo, nodo_inicio, nodo_objetivo, distancias)

    print("***************************************************************************************************************************************************")

    if resultado is not None:
        print(f"Se encontró el nodo objetivo {nodo_objetivo} partiendo del nodo {nodo_inicio} y siguiendo el camino {nodo_inicio} -> {resultado} -> {nodo_objetivo}")
        
        # Encontrar el camino más corto en el grafo
        camino_mas_corto = nx.shortest_path(grafo, nodo_inicio, nodo_objetivo)
        
        # Creamos una nueva ventana para mostrar el grafo con el camino encontrado
        plt.figure()

        # Dibujar el grafo con el camino encontrado
        posicion_nodos = nx.spring_layout(grafo)
        nx.draw(grafo, pos=posicion_nodos, with_labels=True)

        # Dibujar el camino 
        aristas_camino = [(camino_mas_corto[i], camino_mas_corto[i+1]) for i in range(len(camino_mas_corto)-1)]
        nx.draw_networkx_edges(grafo, pos=posicion_nodos, edgelist=aristas_camino, edge_color='r', width=2)
        
        # Agregamos las etiquetas de las distancias en las aristas
        etiquetas = nx.get_edge_attributes(grafo, 'weight')
        nx.draw_networkx_edge_labels(grafo, pos=posicion_nodos, edge_labels=etiquetas)
        
        # Asignamos un nombre a la figura 
        plt.title("Grafo con el camino encontrado")        
        
        # Definimos un objeto manager
        manager = plt.get_current_fig_manager()

        # Asignamos un nombre a la ventana
        manager.set_window_title("Camino encontrado")

        # Cambiamos la posición de la ventana
        manager.window.setGeometry(0, 580, manager.window.width(), manager.window.height())

        # Mostramos ambas ventanas
        plt.show()
    else:
        print(f"No se pudo encontrar el nodo objetivo {nodo_objetivo} partiendo del nodo {nodo_inicio}")
        
        # Mostramos solo la ventana del grafo que se creó
        plt.show()