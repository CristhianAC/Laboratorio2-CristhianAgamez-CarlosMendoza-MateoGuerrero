import folium
import json
import time
from geopy import distance
from opensky_api import OpenSkyApi
from .DijkstraInicioFinOOP import Grafo
import datetime
class AirportMap:
    def __init__(self):
        self.origen = None
        self.api = OpenSkyApi()
        self.now = int(time.time())
        with open("API/city_dataSIU.json", "r") as f:
            self.airports_dict = json.load(f)
        with open("API/icao_dataSIU.json", "r") as l:
            self.icao_dict = json.load(l)
        self.mapa = folium.Map(location=[4.6097100, -74.0817500], min_zoom=3, zoom_start=3, tiles="Stamen Terrain")
        self.icoa_origen = None
        self.etiqueta_origen = None
        self.Grafo = {}
        horaActual = datetime.datetime.now()
        if horaActual.hour == 0 and horaActual.minute == 0:
            with open("API/grafo.json", "w") as h:
                self.crearGrafo()
                json.dump(self.Grafo, h)
                
                
        self.obGrafo = Grafo()
    
    def crearPath(self, origen, fin):
        path = self.obGrafo.shortest_path(origen, fin)
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
            print("La ciudad ingresada no está en la lista de aeropuertos.")
            
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
                        folium.Marker(location=salida, popup=self.etiqueta_origen + " (salida)", icon=folium.Icon(color='darkblue')).add_to(self.mapa)
                        folium.Marker(location=llegada, popup=etiqueta_llegada + " (llegada)", icon=folium.Icon(color='darkpurple')).add_to(self.mapa)
                        etiqueta = f"{self.etiqueta_origen}-{etiqueta_llegada} ({dist_km} km)"
                        folium.PolyLine(locations=[salida, llegada], color='blue', tooltip=etiqueta).add_to(self.mapa)
    
    def mostrar_destino(self, destino):
        icoa_salida = self.icoa_origen
        if destino in self.airports_dict:
            icao_destino = self.airports_dict[destino]['icao']
            etiqueta_destino = self.airports_dict[destino]["city"]
        else:
            print("La ciudad ingresada no está en la lista de aeropuertos.")
            return
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
                        folium.Marker(location=salida, popup=etiqueta_salida + " (salida)", icon=folium.Icon(color='darkblue')).add_to(self.mapa)
                        folium.Marker(location=llegada, popup=etiqueta_destino + " (llegada)", icon=folium.Icon(color='darkpurple')).add_to(self.mapa)
                        etiqueta = f"{self.origen}-{destino} ({dist_km} km)"
                        folium.PolyLine(locations=[salida, llegada], color='blue', tooltip=etiqueta).add_to(self.mapa)
                        self.mapa.fit_bounds([salida, llegada])
                        return
        print(f"No se encontraron vuelos desde {self.origen} a {destino}.")
    
    # Dentro de la clase donde se encuentra la función mostrar_destino()
    def graficar_ciudades(self, lista):
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

            html = f"Capital: {salida}<br> Ruta: {salida}→{llegada} (llegada)<br>Distancia: {distancia} km"
            iframe = folium.IFrame(html, width=200, height=70)
            popup = folium.Popup(iframe, max_width=200)
            marker = folium.Marker(location=coord_salida, popup=popup, icon=folium.Icon(color=color_salida)).add_to(self.mapa)
            folium.Marker(location=coord_llegada, popup=llegada + " (llegada)", icon=folium.Icon(color='darkpurple')).add_to(self.mapa)
            etiqueta = f"{salida} → {llegada}({distancia})"
            folium.PolyLine(locations=[coord_salida, coord_llegada], color='blue', tooltip=etiqueta).add_to(self.mapa)
        return self.mapa


    def mostrar_mapa(self):
        return self.mapa





