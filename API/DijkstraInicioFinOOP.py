import json
import heapq # Para usar la cola de prioridad
# Definir una clase Grafo que representa un grafo ponderado
class Grafo:
    # El constructor recibe un diccionario que representa las aristas y sus pesos
    def __init__(self):
        with open("API/grafo.json", "r") as f:
            self.diccionario = json.load(f)
        
        
    # Un método para obtener los nodos del grafo
    def get_nodos(self):
        return list(self.diccionario.keys())
    
    # Un método para obtener los vecinos de un nodo
    def get_vecinos(self, nodo):
        if nodo is not None:
            return list(self.diccionario[nodo].keys())
        else:
            return []
    
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
        # Crear una cola de prioridad vacía
        cola = []
        # Insertar el origen con distancia 0
        heapq.heappush(cola, (0, origen))
        while cola:     
            # Extraer el nodo con menor distancia
            d, u = heapq.heappop(cola)
            # Marcarlo como visitado
            visitado.add(u)     
            # Comprobar si la distancia es la misma que la almacenada
            if d == distancia[u]:
                # Iterar sobre sus vecinos
                for v in self.diccionario[u]:       
                    if v not in visitado:         
                        d = distancia[u] + self.diccionario[u][v]      
                        if d < distancia.get(v, float("inf")):        
                            distancia[v] = d                
                            previo[v] = u
                            # Insertar el vecino con la nueva distancia
                            heapq.heappush(cola, (d, v))
        return distancia, previo
    def min_distancia(self, distancia, visitado):
        minimo = float("inf")
        nodo_minimo = None
        for nodo in distancia:
            if nodo not in visitado and distancia[nodo] < minimo:
                minimo = distancia[nodo]
                nodo_minimo = nodo
        # Si no hay ningún nodo con distancia menor que infinito, devolver uno cualquiera
        print (nodo_minimo)
        if nodo_minimo == None:
            for nodo in distancia:
                if nodo not in visitado:
                    print("Entre")
                    return nodo
        return nodo_minimo
    
    # Un método para encontrar el camino más corto entre dos nodos usando Dijkstra
    def shortest_path(self, origen, destino):
        # Ejecutar Dijkstra desde el origen
        origeni = self.diccionario.get(origen)
        
        if origeni is not None:
            destinoi = self.diccionario.get(origen).get(destino)
            
            if destinoi is not None:
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

