import folium
import json
import time
from geopy import distance
from opensky_api import OpenSkyApi
from .DijkstraInicioFinOOP import Grafo
import datetime
from collections import deque
class AirportMap:
    def __init__(self):
        self.origen = None
        self.api = OpenSkyApi()
        self.now = int(time.time())
        with open("appDeVuelo/city_dataSIU.json", "r") as f:
            self.airports_dict = json.load(f)
        with open("appDeVuelo/icao_dataSIU.json", "r") as l:
            self.icao_dict = json.load(l)
        self.mapa = folium.Map(location=[4.6097100, -74.0817500], min_zoom=3, zoom_start=3, tiles="Stamen Terrain")
        self.icoa_origen = None
        self.etiqueta_origen = None
        self.Grafo = {}
        self.horaActual = datetime.datetime.now()
        
        ahora = datetime.datetime.now()
        
        
        
        self.error = ""
        for icao, airport in self.airports_dict.items():
            folium.Marker([airport['lat'], airport['lon']], popup= airport["city"], icon=folium.Icon(color='lightgray')).add_to(self.mapa)
        fileHora = open("appDeVuelo/ultimavez.txt", "r")
        
        
        
        if  int(fileHora.read()) != int(ahora.day): 
            
            t = open("appDeVuelo/ultimavez.txt", "w")
            t.write(str(ahora.day))
            t.close
            with open("appDeVuelo/grafo.json", "w") as h:
                self.crearGrafo()
                json.dump(self.Grafo, h)
        
        
        fileHora.close()
        
        self.obGrafo = Grafo()
        self.Grafo = self.obGrafo.diccionario
    
    def crearPath(self, origen, fin):
        path = self.obGrafo.shortest_path(origen, fin)
        if path is not None:
            self.error = ""
        return path
    def crearGrafo(self):
        
        for airport in self.airports_dict.values():
            self.Grafo[airport["icao"]] = {}
            flights = self.api.get_departures_by_airport(airport["icao"], begin=self.now-2*(24*3600), end=self.now)
            
            for flight in flights:
                if flight.estArrivalAirport is not None:
                    
                    arrival = self.icao_dict.get(flight.estArrivalAirport)
                    
                    if arrival is not None:
                        salida = (airport["lat"], airport["lon"])
                        
                        llegada = (arrival["lat"], arrival["lon"])
                        self.Grafo[airport["icao"]][flight.estArrivalAirport] = round(distance.distance(salida, llegada).km, 2)
        
        
        

    
        


    def mostrar_todos_destinos(self, origen):
        self.origen = origen
        if self.origen in self.airports_dict:
            self.icoa_origen = self.airports_dict[self.origen]['icao']
            self.etiqueta_origen = self.airports_dict[self.origen]["city"]
        else:
            print("Entré")
            self.error = "La ciudad ingresada no está en la lista de aeropuertos."
        grupo = folium.FeatureGroup(name="Destinos")
        for icao, airport in self.airports_dict.items():
            folium.Marker([airport['lat'], airport['lon']], popup= airport["city"], icon=folium.Icon(color='lightgray')).add_to(self.mapa)
        
        flights = self.api.get_departures_by_airport(self.icoa_origen, begin=self.now-2*(24*3600), end=self.now)
        for flight in flights: 
            if flight.estArrivalAirport is not None:
                for airport in self.airports_dict.values():
                    if airport["icao"] == flight.estDepartureAirport:
                        salida = (airport["lat"], airport["lon"]) 
                    if airport["icao"] == flight.estArrivalAirport:
                        llegada = (airport["lat"], airport["lon"])
                        dist_km = round(distance.distance(salida, llegada).km, 2)
                        etiqueta_llegada = airport["city"]
                        grupo.add_child(folium.Marker(location=salida, popup=self.etiqueta_origen + " (salida)", icon=folium.Icon(color='darkblue')))
                        grupo.add_child(folium.Marker(location=llegada, popup=etiqueta_llegada + " (llegada)", icon=folium.Icon(color='darkpurple')))
                        etiqueta = f"{self.etiqueta_origen}-{etiqueta_llegada} ({dist_km} km)"
                        grupo.add_child(folium.PolyLine(locations=[salida, llegada], color='blue', tooltip=etiqueta))
                        self.mapa.add_child(grupo)
                        
    
    def mostrar_destino(self, destino):
        icoa_salida = self.icoa_origen
        if destino in self.airports_dict:
            icao_destino = self.airports_dict[destino]['icao']
            etiqueta_destino = self.airports_dict[destino]["city"]
        else:
            self.error =("La ciudad ingresada no está en la lista de aeropuertos.")
            return
        grupo2 = folium.FeatureGroup(name="Destinos")
        flights = self.api.get_departures_by_airport(icoa_salida, begin=self.now-2*(24*3600), end=self.now)
        for flight in flights:
            if flight.estArrivalAirport == icao_destino:
                for airport in self.airports_dict.values():
                    if airport["icao"] == flight.estDepartureAirport:
                        salida = (airport["lat"], airport["lon"])
                        etiqueta_salida = airport["city"]
                    if airport["icao"] == flight.estArrivalAirport:
                        llegada = (airport["lat"], airport["lon"])
                        etiqueta_destino = airport["city"]
                        dist_km = round(distance.distance(salida, llegada).km, 2)
                        grupo2.add_child(folium.Marker(location=salida, popup=etiqueta_salida + " (salida)", icon=folium.Icon(color='darkblue')))
                        grupo2.add_child(folium.Marker(location=llegada, popup=etiqueta_destino + " (llegada)", icon=folium.Icon(color='darkpurple')))
                        etiqueta = f"{self.origen}-{destino} ({dist_km} km)"
                        grupo2.add_child(folium.PolyLine(locations=[salida, llegada], color='blue', tooltip=etiqueta))
                        self.mapa.fit_bounds([salida, llegada])
                        self.error = ""
                        self.mapa.add_child(grupo2)
                        return
        self.error = f"No se encontraron vuelos desde {self.origen} a {destino}."
    
    # Dentro de la clase donde se encuentra la función mostrar_destino()
    def graficar_ciudades(self, lista):
        if not hasattr (self, 'objetos'):
            self.objetos = []
        # Si hay objetos anteriores, borrarlos
        for obj in self.objetos:
            obj.remove ()
        # Vaciar la lista de objetos
        self.objetos = []

        for icao, airport in self.airports_dict.items():
            folium.Marker([airport['lat'], airport['lon']], popup= airport["city"], icon=folium.Icon(color='lightgray')).add_to(self.mapa)

        for i, ciudad in enumerate(lista[:-1]):
            salida = lista[i]
            llegada = lista[i + 1]
            coord_salida = [self.icao_dict[salida]["lat"], self.icao_dict[salida]["lon"]]
            coord_llegada = [self.icao_dict[llegada]["lat"], self.icao_dict[llegada]["lon"]]
            distancia = round(distance.distance(coord_salida, coord_llegada).km, 2)
            if i == 0:
                color_salida = "green"
            else:
                color_salida = "darkblue"
            nombreSalida = self.icao_dict[salida]['city']
            nombreLlegada = self.icao_dict[llegada]['city']
            html = f"Capital: {nombreSalida}<br> Ruta: {nombreSalida}→{nombreLlegada}<br>Distancia: {distancia} km"
            iframe = folium.IFrame(html, width=200, height=70)
            popup = folium.Popup(iframe, max_width=200)
            
            # Crear los marcadores y la línea
            marcador_salida = folium.Marker(location=coord_salida, popup=popup, icon=folium.Icon(color=color_salida))
            marcador_llegada = folium.Marker(location=coord_llegada, popup=nombreLlegada, icon=folium.Icon(color='darkpurple'))
            etiqueta = f"{salida} → {llegada}({distancia})"
            linea = folium.PolyLine(locations=[coord_salida, coord_llegada], color='blue', tooltip=etiqueta)

            # Añadir los objetos al mapa y a la lista de objetos
            marcador_salida.add_to(self.mapa)
            marcador_llegada.add_to(self.mapa)
            linea.add_to(self.mapa)
            self.objetos.append(marcador_salida)
            self.objetos.append(marcador_llegada)
            self.objetos.append(linea)

        return self.mapa
    def bfs(self, inicio):
        visitados = []
        cola = deque([inicio])
        while cola:
            nodo = cola.popleft()
            if nodo not in visitados:
                visitados.append(nodo)
                print(nodo)
                for vecino in self.Grafo[nodo].keys():
                    if vecino not in visitados:
                        cola.append(vecino)
        return visitados
    def dfs(self, inicio):
        visited = set()
        stack = [inicio]
        path = []
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                path.append(node)
                stack.extend(reversed(list(self.Grafo[node].keys())))
        
        return path
    def dfsGraphic(self, inicio):
        lista = self.dfs(self.airports_dict[inicio]['icao'])
        self.graficar_ciudades(lista)
    def bfsGraphic(self, inicio):
        lista = self.bfs(self.airports_dict[inicio]['icao'])
        self.graficar_ciudades(lista)

    def mostrar_mapa(self):
        return self.mapa





