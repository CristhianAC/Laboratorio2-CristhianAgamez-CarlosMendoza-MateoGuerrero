from django.shortcuts import render
from django.http import HttpResponse

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
            'error' : flight.error,
        }
        return render(request, 'sistema.html', context)
    else:
        if request.POST["destiny"]:
            try:
                flight.graficar_ciudades(flight.crearPath(flight.airports_dict[request.POST["City"]]["icao"] ,flight.airports_dict[request.POST["destiny"]]["icao"] )) 
            except:
                flight.error = "Una de las ciudades digitadas no existe"
        else:
            
            flight.mostrar_todos_destinos(request.POST["City"])
            print(flight.error)

        m = m._repr_html_()

        context = {
            'm': m,
            'addCity': addCity(),
            'error': flight.error,

        }
        return render(request, 'sistema.html', context)
