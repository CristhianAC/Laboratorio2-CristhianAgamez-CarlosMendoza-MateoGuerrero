from opensky_api import OpenSkyApi
import folium
import json
import time
from geopy import distance

api = OpenSkyApi()
now = int(time.time())

with open("yatusabe.json", "r") as f: 
    airports_dict = json.load(f)

mapa = folium.Map(location=[4.6097100, -74.0817500], min_zoom=3, zoom_start=3, tiles="Stamen Terrain")

city = input("Ingrese el nombre de la ciudad: ")
if city in airports_dict:
    icao = airports_dict[city]['icao']
    etiqueta_salida = airports_dict[city]["city"]
else:
    print("La ciudad ingresada no está en la lista de aeropuertos.")
    exit()

flights = api.get_departures_by_airport(icao, begin=now-2*(24*3600), end=now)

for icao, airport in airports_dict.items():
    folium.Marker([airport['lat'], airport['lon']], icon=folium.Icon(color='lightgray')).add_to(mapa)

for flight in flights: 
    if flight.estArrivalAirport is not None:
        for airport in airports_dict.values():
            if airport["icao"] == flight.estDepartureAirport:
                salida = (airport["lat"], airport["lon"]) 
            if airport["icao"] == flight.estArrivalAirport:
                llegada = (airport["lat"], airport["lon"])
                dist_km = round(distance.distance(salida, llegada).km, 2)
                etiqueta_llegada = airport["city"]
                folium.Marker(location=salida, popup=etiqueta_salida + " (salida)", icon=folium.Icon(color='darkblue')).add_to(mapa)
                folium.Marker(location=llegada, popup=etiqueta_llegada + " (llegada)", icon=folium.Icon(color='darkpurple')).add_to(mapa)
                etiqueta = f"{flight.estArrivalAirport} ({dist_km} km)"
                folium.PolyLine(locations=[salida, llegada], color='blue', tooltip=etiqueta).add_to(mapa)

mapa
mapa.save('mapa.html')
