# Definir una clase Grafo que representa un grafo ponderado
class Grafo:
    # El constructor recibe un diccionario que representa las aristas y sus pesos
    def __init__(self, diccionario):
        self.diccionario = diccionario
    
    # Un método para obtener los nodos del grafo
    def get_nodos(self):
        return list(self.diccionario.keys())
    
    # Un método para obtener los vecinos de un nodo
    def get_vecinos(self, nodo):
        if nodo is not None:
            return list(self.diccionario[nodo].keys())
        else:
            return None
    
    # Un método para obtener el peso de una arista
    def get_peso(self, origen, destino):
        return self.diccionario[origen][destino]
    
    # Un método para aplicar el algoritmo de Dijkstra desde un nodo origen
    def dijkstra(self, origen):
        distancia = {}  
        previo = {}  
        visitado = set()  
        distancia[origen] = 0
        previo[origen] = None  
        while len(visitado) < len(self.get_nodos()):     
            u = self.min_distancia(distancia, visitado)    
            visitado.add(u)     
            if (self.get_vecinos(u) is not None):
                for v in self.get_vecinos(u):       
                    if v not in visitado:         
                        d = distancia[u] + self.get_peso(u, v)      
                        if d < distancia.get(v, float("inf")):        
                            distancia[v] = d                
                            previo[v] = u
        return distancia, previo
    
    # Un método auxiliar para encontrar el nodo con la menor distancia que no ha sido visitado
    def min_distancia(self, distancia, visitado): 
        minimo = float("inf")
        nodo_minimo = None 
        for nodo in distancia:    
            if nodo not in visitado and distancia[nodo] < minimo:        
                minimo = distancia[nodo]
                nodo_minimo = nodo
        return nodo_minimo
    
    # Un método para encontrar el camino más corto entre dos nodos usando Dijkstra
    def shortest_path(self, origen, destino):
        # Ejecutar Dijkstra desde el origen
        origenFin = self.diccionario.get(origen).get(destino)
        if origenFin is not None:
            return [origen, destino]
        distancia, previo = self.dijkstra(origen)
        # Verificar si el destino es alcanzable
        if destino not in distancia:
            return None
        # Retroceder el camino desde el destino al origen
        path = [destino]
        while previo[destino] != None:
            destino = previo[destino]
            path.append(destino)
        # Invertir el camino para obtener el orden correcto
        path.reverse()
        return path

# Crear un objeto Grafo con el diccionario dado
"""
grafo = Grafo({
    "a": {"b": 1, "c": 3},
    "b": {"a": 1, "c": 1, "d": 4},
    "c": {"a": 3, "b": 1, "d": 2, "e": 3},
    "d": {"b": 4, "c": 2, "e": 2, "f": 1},
    "e": {"c": 3, "d": 2, "f": 3, "g": 2},
    "f": {"d": 1, "e": 3, "g": 4},
    "g": {"e": 2, "f": 4}
})
"""

# Ejemplo: encontrar el camino más corto desde a hasta g
"""
path = grafo.shortest_path("a", "g")
if path:
    print("El camino más corto desde a hasta g es:", "->".join(path))
else:
    print("No hay camino desde a hasta g")
"""