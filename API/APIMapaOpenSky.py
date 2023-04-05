# Importar el módulo opensky_api
from opensky_api import OpenSkyApi

# Importar la biblioteca folium para el mapa interactivo
import folium

# Importar la biblioteca json para leer el archivo de aeropuertos
import json

# Crear una instancia de la API
api = OpenSkyApi()

# Obtener la hora actual en segundos desde la época
import time 
now = int(time.time())

# Obtener los vuelos que salieron de LEMD en las últimas 24 horas
flights = api.get_departures_by_airport("LEMD", begin=now-4*(24*3600), end=now)

# Leer el archivo de aeropuertos y crear un diccionario con los códigos IATA como claves
with open("aeropuertos.json", "r") as f: 
    airports = json.load(f)

# Crear un mapa mundial centrado en Madrid
mapa = folium.Map(location=[40.4167754, -3.7037902], zoom_start=3)

# Agregar marcadores para cada vuelo
for flight in flights: 
    if flight.estArrivalAirport is not None: 
        # Obtener las coordenadas de la salida y la llegada del vuelo usando el diccionario de aeropuertos 
        salida = (airports[flight.estDepartureAirport]["lat"], airports[flight.estDepartureAirport]["lon"]) 
        llegada = (airports[flight.estArrivalAirport]["lat"], airports[flight.estArrivalAirport]["lon"])

        # Crear un marcador para la salida del vuelo
        folium.Marker(location=salida, popup=flight.estArrivalAirport + " (salida)", icon=folium.Icon(color='green')).add_to(mapa)

        # Crear un marcador para la llegada del vuelo
        folium.Marker(location=llegada, popup=flight.estArrivalAirport + " (llegada)", icon=folium.Icon(color='red')).add_to(mapa)

        # Crear una línea entre la salida y la llegada del vuelo
        folium.PolyLine(locations=[salida, llegada], color='blue').add_to(mapa)

# Mostrar el mapa
mapa
mapa.save('mapa.html')