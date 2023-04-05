# Importar el módulo opensky_api
from opensky_api import OpenSkyApi

# Crear una instancia de la API
api = OpenSkyApi()

# Obtener la hora actual en segundos desde la época
import time
now = int(time.time())

# Obtener los vuelos que salieron de LEMD en las últimas 24 horas
flights = api.get_departures_by_airport("MMMX", begin=now-24*3600, end=now)

# Imprimir el número de vuelos y sus destinos
print(f"Se encontraron {len(flights)} vuelos desde LEMD.")
for flight in flights:
    if flight.estArrivalAirport is None:
        print(f"El vuelo {flight.callsign} salió a las {flight.estDepartureAirportHorizDistance} pero no se sabe su destino.")
    else:
        print(f"El vuelo {flight.callsign} salió a las {flight.estDepartureAirportHorizDistance} y llegó a {flight.estArrivalAirport}.")