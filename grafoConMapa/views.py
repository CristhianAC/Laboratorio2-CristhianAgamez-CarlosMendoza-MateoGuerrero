from django.shortcuts import render
from django.http import HttpResponse

from .forms import addCity
from API.ApiNodosOOP import AirportMap
# Create
# your views here.


def index(request):
    
    
    return render(request, 'index.html', {})


def mapa(request):
    
    
    

    if request.method == "GET":
        flight = AirportMap()
        m = flight.mostrar_mapa()
        m = m._repr_html_()

        context = {
            'm': m,
            'addCity': addCity(),
            'error' : flight.error,
            'flight': flight,
        }
        return render(request, 'sistema.html', context)
    else:
        flight = AirportMap()
        if request.POST["destiny"] and request.POST["City"]:
            try:
                flight.graficar_ciudades(flight.crearPath(flight.airports_dict[request.POST["City"]]["icao"] ,flight.airports_dict[request.POST["destiny"]]["icao"] )) 
            except:
                flight.error = "Una de las ciudades digitadas no existe"
        else:
            if request.POST['bfs']:
                flight.bfsGraphic(request.POST['bfs'])
            else:    
                flight.mostrar_todos_destinos(request.POST["City"])
                print(flight.error)
        m = flight.mostrar_mapa()
        m = m._repr_html_()

        context = {
            'm': m,
            'addCity': addCity(),
            'error': flight.error,
            'flight': flight,

        }
        return render(request, 'sistema.html', context)
