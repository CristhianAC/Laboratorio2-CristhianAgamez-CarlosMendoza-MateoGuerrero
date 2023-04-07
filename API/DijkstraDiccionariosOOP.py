# Definir la clase Grafo
class Grafo:
    # Inicializar el grafo con un diccionario de nodos y aristas
    def __init__(self, grafo):
        self.grafo = grafo # Un diccionario con los nodos como claves y sus vecinos y pesos como valores

    # Definir un método auxiliar para encontrar el nodo con la menor distancia
    # entre los nodos no visitados
    def min_distancia(self, distancia, visitado):
        # Inicializar el mínimo y el nodo mínimo
        minimo = float("inf")
        nodo_minimo = None
        # Recorrer todos los nodos del grafo
        for nodo in self.grafo:
            # Si el nodo no ha sido visitado y su distancia es menor que el mínimo
            if nodo not in visitado and distancia[nodo] < minimo:
                # Actualizar el mínimo y el nodo mínimo
                minimo = distancia[nodo]
                nodo_minimo = nodo
        # Devolver el nodo mínimo
        return nodo_minimo

    # Definir el método principal para el algoritmo de Dijkstra
    def dijkstra(self, origen):
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
        while len(visitado) < len(self.grafo):
            # Encontrar el nodo con la menor distancia entre los no visitados
            u = self.min_distancia(distancia, visitado)
            # Marcarlo como visitado
            visitado.add(u)
            # Recorrer todos los nodos adyacentes a u
            for v in self.grafo[u]:
                # Si v no ha sido visitado
                if v not in visitado:
                    # Calcular la distancia desde u a v como la suma de la distancia desde el origen a u y el peso de la arista entre u y v
                    d = distancia[u] + self.grafo[u][v]
                    # Si esta distancia es menor que la distancia actual desde el origen a v
                    if d < distancia.get(v, float("inf")):
                        # Actualizar la distancia desde el origen a v con el nuevo valor
                        distancia[v] = d
                        # Actualizar el nodo previo a v con u
                        previo[v] = u
        # Devolver los diccionarios de distancia y previo
        return distancia, previo

# Crear un grafo con el diccionario del ejemplo anterior

grafo = {
    "a": {"b": 1, "c": 3},
    "b": {"a": 1, "c": 1, "d": 4},
    "c": {"a": 3, "b": 1, "d": 2, "e": 3},
    "d": {"b": 4, "c": 2, "e": 2, "f": 1},
    "e": {"c": 3, "d": 2, "f": 3, "g": 2},
    "f": {"d": 1, "e": 3, "g": 4},
    "g": {"e": 2, "f": 4}
}

# Llamar al método dijkstra con el grafo y el nodo origen
distancia, previo = Grafo(grafo).dijkstra("a")

# Imprimir los resultados
print("Distancia desde a a cada nodo:")
for nodo in distancia:
    print(nodo, ":", distancia[nodo])

print("Nodo previo a cada nodo:")
for nodo in previo:
    print(nodo, ":", previo[nodo])