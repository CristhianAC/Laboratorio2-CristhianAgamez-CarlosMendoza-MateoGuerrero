from opensky_api import OpenSkyApi
import folium
import json
import time
from geopy import distance

class AirportMap:
    def __init__(self):
        self.icao = None
        self.api = OpenSkyApi()
        self.now = int(time.time())
        with open("API/Capitales.json", "r") as f: 
            self.airports_dict = json.load(f)
        self.mapa = folium.Map(location=[4.6097100, -74.0817500], min_zoom=3, zoom_start=3, tiles="Stamen Terrain")
        self.add_airport_markers()
        
        
    def actualizar(self, icao =  "SKBO"):
        self.icao = icao
        print(icao)
        self.add_flight_markers()
    def add_airport_markers(self):
        for icao, airport in self.airports_dict.items():
            folium.Marker([airport['lat'], airport['lon']], icon=folium.Icon(color='lightgray')).add_to(self.mapa)

    def add_flight_markers(self):
        flights = self.api.get_departures_by_airport(self.icao, begin=self.now-2*(24*3600), end=self.now)
        for flight in flights: 
            if flight.estArrivalAirport is not None and flight.estArrivalAirport in self.airports_dict: 
                salida = (self.airports_dict[flight.estDepartureAirport]["lat"], self.airports_dict[flight.estDepartureAirport]["lon"]) 
                llegada = (self.airports_dict[flight.estArrivalAirport]["lat"], self.airports_dict[flight.estArrivalAirport]["lon"])
                dist_km = round(distance.distance(salida, llegada).km, 2)
                folium.Marker(location=salida, popup=flight.estArrivalAirport + " (salida)", icon=folium.Icon(color='darkblue')).add_to(self.mapa)
                folium.Marker(location=llegada, popup=flight.estArrivalAirport + " (llegada)", icon=folium.Icon(color='darkpurple')).add_to(self.mapa)
                etiqueta = f"{flight.estArrivalAirport} ({dist_km} km)"
                folium.PolyLine(locations=[salida, llegada], color='blue', tooltip=etiqueta).add_to(self.mapa)

    def show_map(self):
        
        return self.mapa



