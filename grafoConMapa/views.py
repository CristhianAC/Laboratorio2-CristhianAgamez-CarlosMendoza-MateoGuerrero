from django.shortcuts import render
from django.http import HttpResponse
import folium
from .forms import addCity
from API.ApiNodosOOP import AirportMap
# Create
# your views here.
flight = AirportMap()

def index(request):
    
    
    return render(request, 'index.html', {})


def mapa(request):
    
    
    m = flight.mostrar_mapa()

    if request.method == "GET":
        m = m._repr_html_()

        context = {
            'm': m,
            'addCity': addCity(),

        }
        return render(request, 'sistema.html', context)
    else:
        if request.POST["destiny"]:
            
            print(flight.crearPath(flight.airports_dict[request.POST["City"]]["icao"] ,flight.airports_dict[request.POST["destiny"]]["icao"] ))
            
        else:
            flight.mostrar_todos_destinos(request.POST["City"])

        m = m._repr_html_()

        context = {
            'm': m,
            'addCity': addCity(),

        }
        return render(request, 'sistema.html', context)
