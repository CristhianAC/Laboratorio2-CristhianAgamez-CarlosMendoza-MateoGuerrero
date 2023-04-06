import folium
import json
import time
from geopy import distance
from opensky_api import OpenSkyApi

class FlightMap:
    def __init__(self, origen):
        self.origen = origen
        self.api = OpenSkyApi()
        self.now = int(time.time())
        with open("city_dataSIU.json", "r") as f:
            self.airports_dict = json.load(f)
        self.mapa = folium.Map(location=[4.6097100, -74.0817500], min_zoom=3, zoom_start=3, tiles="Stamen Terrain")
        if self.origen in self.airports_dict:
            self.icoa_origen = self.airports_dict[self.origen]['icao']
            self.etiqueta_origen = self.airports_dict[self.origen]["city"]
        else:
            print("La ciudad ingresada no está en la lista de aeropuertos.")
            exit()
        for icao, airport in self.airports_dict.items():
            folium.Marker([airport['lat'], airport['lon']], popup= airport["city"], icon=folium.Icon(color='lightgray')).add_to(self.mapa)
    
    def mostrar_todos_destinos(self):
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
    """
    def mostrar_destinos_consecutivos(self):
        icoa_salida = self.icoa_origen
        while True:
            destino = input("Ingrese el nombre de la ciudad de destino (ingrese '9' para terminar): ")
            if destino == '9':
                break
            else:
                if destino in self.airports_dict:
                    icao_destino = self.airports_dict[destino]['icao']
                    etiqueta_destino = self.airports_dict[destino]["city"]
                else:
                    print("La ciudad ingresada no está en la lista de aeropuertos.")
                    continue
                flights = self.api.get_departures_by_airport(icoa_salida, begin=self.now-2*(24*3600), end=self.now)
                for flight in flights:
                    if flight.estArrivalAirport == icao_destino:
                        for airport in self.airports_dict.values():
                            if airport["icao"] == flight.estDepartureAirport:
                                salida = (airport["lat"], airport["lon"])
                                etiqueta_salida = airport["city"]
                            if airport["icao"] == flight.estArrivalAirport:
                                llegada = (airport["lat"], airport["lon"])
                        dist_km = round(distance.distance(salida, llegada).km, 2)
                        folium.Marker(location=salida, popup=etiqueta_salida + " (salida)", icon=folium.Icon(color='darkblue')).add_to(self.mapa)
                        folium.Marker(location=llegada, popup=etiqueta_destino + " (llegada)", icon=folium.Icon(color='darkpurple')).add_to(self.mapa)
                        etiqueta = f"{flight.estArrivalAirport} ({dist_km} km)"
                        folium.PolyLine(locations=[salida, llegada], color='blue', tooltip=etiqueta).add_to(self.mapa)
            icoa_salida = icao_destino
    """   
    def mostrar_mapa(self):
        self.mapa.save("flight_map.html")
        print("El mapa se ha generado correctamente en el archivo 'flight_map.html'.")
    


origen = input("Origen: ")
#destino = input("Destino: ")
mapa_vuelos = FlightMap(origen)
mapa_vuelos.mostrar_destinos_consecutivos()
mapa_vuelos.mostrar_mapa()

