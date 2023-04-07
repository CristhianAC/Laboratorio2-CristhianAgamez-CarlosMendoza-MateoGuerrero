grafo = {
    "a": {"b": 1, "c": 3},
    "b": {"a": 1, "c": 1, "d": 4},
    "c": {"a": 3, "b": 1, "d": 2, "e": 3},
    "d": {"b": 4, "c": 2, "e": 2, "f": 1},
    "e": {"c": 3, "d": 2, "f": 3, "g": 2},
    "f": {"d": 1, "e": 3, "g": 4},
    "g": {"e": 2, "f": 4}
}

def min_distancia(distancia, visitado): 
    minimo = float("inf")
    nodo_minimo = None 
    for nodo in distancia:    
        if nodo not in visitado and distancia[nodo] < minimo:        
            minimo = distancia[nodo]
            nodo_minimo = nodo
    return nodo_minimo

def dijkstra(grafo, origen):   
    distancia = {}  
    previo = {}  
    visitado = set()  
    distancia[origen] = 0
    previo[origen] = None  
    while len(visitado) < len(grafo):     
        u = min_distancia(distancia, visitado)    
        visitado.add(u)     
        for v in grafo[u]:       
            if v not in visitado:         
                d = distancia[u] + grafo[u][v]      
                if d < distancia.get(v, float("inf")):        
                    distancia[v] = d                
                    previo[v] = u
    return distancia, previo

def shortest_path(grafo, origen, destino):
    # Run dijkstra from the origin node
    distancia, previo = dijkstra(grafo, origen)
    # Check if the destination node is reachable
    if destino not in distancia:
        return None
    # Trace back the path from the destination to the origin
    path = [destino]
    while previo[destino] != None:
        destino = previo[destino]
        path.append(destino)
    # Reverse the path to get the correct order
    path.reverse()
    return path

# Example: find the shortest path from a to g
path = shortest_path(grafo, "a", "g")
if path:
    print("The shortest path from a to g is:", "->".join(path))
else:
    print("There is no path from a to g")