# Definir el grafo como un diccionario
# Las claves son los nodos y los valores son diccionarios
# con los nodos adyacentes y sus distancias
grafo = {
    "a": {"b": 1, "c": 3},
    "b": {"a": 1, "c": 1, "d": 4},
    "c": {"a": 3, "b": 1, "d": 2, "e": 3},
    "d": {"b": 4, "c": 2, "e": 2, "f": 1},
    "e": {"c": 3, "d": 2, "f": 3, "g": 2},
    "f": {"d": 1, "e": 3, "g": 4},
    "g": {"e": 2, "f": 4}
}

# Definir una función auxiliar para encontrar el nodo con la menor distancia
# entre los nodos no visitados
def min_distancia(distancia, visitado):
    # Inicializar el mínimo y el nodo mínimo
    minimo = float("inf")
    nodo_minimo = None
    # Recorrer todos los nodos del grafo
    for nodo in distancia:
        # Si el nodo no ha sido visitado y su distancia es menor que el mínimo
        if nodo not in visitado and distancia[nodo] < minimo:
            # Actualizar el mínimo y el nodo mínimo
            minimo = distancia[nodo]
            nodo_minimo = nodo
    # Devolver el nodo mínimo
    return nodo_minimo

# Definir la función principal para el algoritmo de Dijkstra
def dijkstra(grafo, origen):
    # Inicializar un diccionario para almacenar las distancias desde el origen
    distancia = {}
    # Inicializar un diccionario para almacenar los nodos previos en el camino más corto
    previo = {}
    # Inicializar un conjunto para almacenar los nodos visitados
    visitado = set()
    # Asignar la distancia desde el origen a sí mismo como cero
    distancia[origen] = 0
    # Asignar el nodo previo al origen como ninguno
    previo[origen] = None
    # Mientras haya nodos no visitados en el grafo
    while len(visitado) < len(grafo):
        # Encontrar el nodo con la menor distancia entre los no visitados
        u = min_distancia(distancia, visitado)
        # Marcarlo como visitado
        visitado.add(u)
        # Recorrer todos los nodos adyacentes a u
        for v in grafo[u]:
            # Si el nodo v no ha sido visitado
            if v not in visitado:
                # Calcular la distancia desde u a v como la suma de la distancia desde el origen a u y la distancia desde u a v
                d = distancia[u] + grafo[u][v]
                # Si esta distancia es menor que la distancia actual desde el origen a v
                if d < distancia.get(v, float("inf")):
                    # Actualizar la distancia desde el origen a v con el nuevo valor
                    distancia[v] = d
                    # Actualizar el nodo previo a v con u
                    previo[v] = u
    # Devolver los diccionarios de distancia y previo
    return distancia, previo

# Llamar a la función dijkstra con el grafo y el nodo origen
distancia, previo = dijkstra(grafo, "a")

# Imprimir los resultados
print("Distancia desde a a cada nodo:")
for nodo in distancia:
    print(nodo, ":", distancia[nodo])

print("Nodo previo a cada nodo:")
for nodo in previo:
    print(nodo, ":", previo[nodo])