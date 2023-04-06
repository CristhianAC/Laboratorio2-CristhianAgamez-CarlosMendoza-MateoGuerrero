import folium
import json
import time
from geopy import distance
from opensky_api import OpenSkyApi
api = OpenSkyApi()
now = int(time.time())
with open("city_dataSIU.json", "r") as f:
    airports_dict = json.load(f)
mapa = folium.Map(location=[4.6097100, -74.0817500], min_zoom=3, zoom_start=3, tiles="Stamen Terrain")
origen = input("Ingrese el nombre de la ciudad de origen: ")
if origen in airports_dict:
    icao_origen = airports_dict[origen]['icao']
    etiqueta_origen = airports_dict[origen]["city"]
else:
    print("La ciudad ingresada no está en la lista de aeropuertos.")
    exit()
for icao, airport in airports_dict.items():
    folium.Marker([airport['lat'], airport['lon']], popup= airport["city"], icon=folium.Icon(color='lightgray')).add_to(mapa)
modo = input("Escrbe '1' para mostrar todos los destinos o '2' para mostrar un destino o consecutivamente si están disponibles (escribe '9' para terminar): ")
if modo == '1':
    flights = api.get_departures_by_airport(icao_origen, begin=now-2*(24*3600), end=now)
    for flight in flights: 
        if flight.estArrivalAirport is not None:
            for airport in airports_dict.values():
                if airport["icao"] == flight.estDepartureAirport:
                    salida = (airport["lat"], airport["lon"]) 
                if airport["icao"] == flight.estArrivalAirport:
                    llegada = (airport["lat"], airport["lon"])
                    dist_km = round(distance.distance(salida, llegada).km, 2)
                    etiqueta_llegada = airport["city"]
                    folium.Marker(location=salida, popup=etiqueta_origen + " (salida)", icon=folium.Icon(color='darkblue')).add_to(mapa)
                    folium.Marker(location=llegada, popup=etiqueta_llegada + " (llegada)", icon=folium.Icon(color='darkpurple')).add_to(mapa)
                    etiqueta = f"{flight.estArrivalAirport} ({dist_km} km)"
                    folium.PolyLine(locations=[salida, llegada], color='blue', tooltip=etiqueta).add_to(mapa)
                    
elif modo == '2':
    icoa_salida = icao_origen
    while True:
        destino = input("Ingrese el nombre de la ciudad de destino (ingrese '9' para terminar): ")
        if destino == '9':
            break
        else:
            if destino in airports_dict:
                icao_destino = airports_dict[destino]['icao']
                etiqueta_destino = airports_dict[destino]["city"]
            else:
                print("La ciudad ingresada no está en la lista de aeropuertos.")
                continue
            flights = api.get_departures_by_airport(icoa_salida, begin=now-2*(24*3600), end=now)
            for flight in flights:
                if flight.estArrivalAirport == icao_destino:
                    for airport in airports_dict.values():
                        if airport["icao"] == flight.estDepartureAirport:
                            salida = (airport["lat"], airport["lon"])
                            etiqueta_salida = airport["city"]
                        if airport["icao"] == flight.estArrivalAirport:
                            llegada = (airport["lat"], airport["lon"])
                    dist_km = round(distance.distance(salida, llegada).km, 2)
                    folium.Marker(location=salida, popup=etiqueta_salida + " (salida)", icon=folium.Icon(color='darkblue')).add_to(mapa)
                    folium.Marker(location=llegada, popup=etiqueta_destino + " (llegada)", icon=folium.Icon(color='darkpurple')).add_to(mapa)
                    etiqueta = f"{flight.estArrivalAirport} ({dist_km} km)"
                    folium.PolyLine(locations=[salida, llegada], color='blue', tooltip=etiqueta).add_to(mapa)
        icoa_salida = icao_destino



mapa.save("mapa.html")