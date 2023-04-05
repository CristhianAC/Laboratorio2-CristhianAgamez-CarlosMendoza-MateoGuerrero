from opensky_api import OpenSkyApi
import folium
import json
import time

class FlightMap:
    def __init__(self, airport_code = "LEMD"):
        self.airport_code = airport_code
        self.api = OpenSkyApi()
        self.airports = {}
        self.flights = []
        self.map = None
        
    def _get_airports(self):
        with open("API/aeropuertos.json", "r") as f:
            self.airports = json.load(f)
    
    def _get_flights(self):
        now = int(time.time())
        self.flights = self.api.get_departures_by_airport(self.airport_code, begin=now-4*(24*3600), end=now)
    
    def _create_markers(self):
        for flight in self.flights:
            if flight.estArrivalAirport is not None:          
                salida = (self.airports[flight.estDepartureAirport]["lat"], self.airports[flight.estDepartureAirport]["lon"]) 
                llegada = (self.airports[flight.estArrivalAirport]["lat"], self.airports[flight.estArrivalAirport]["lon"])             
                folium.Marker(location=salida, popup=flight.estArrivalAirport + " (salida)", icon=folium.Icon(color='green')).add_to(self.map)          
                folium.Marker(location=llegada, popup=flight.estArrivalAirport + " (llegada)", icon=folium.Icon(color='red')).add_to(self.map)      
                folium.PolyLine(locations=[salida, llegada], color='blue').add_to(self.map)         
        self.map.save('mapa.html')  

    def create_map(self):
        
        self._get_airports()
        self._get_flights()  
        airport_coords = (self.airports[self.airport_code]["lat"], self.airports[self.airport_code]["lon"])
        self.map = folium.Map(location=airport_coords,min_zoom=3, max_zoom=3)
        self._create_markers()       
        return self.map

flight_map = FlightMap("LEMD")
flight_map.create_map()

