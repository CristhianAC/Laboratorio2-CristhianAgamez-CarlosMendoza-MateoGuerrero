from django.shortcuts import render
from django.http import HttpResponse
import folium
from .forms import addCity
from API.ApiNodosOOP import AirportMap
# Create
# your views here.


def index(request):
    return render(request, 'index.html', {})


def mapa(request):
    flight = AirportMap()
    m = flight.show_map()

    if request.method == "GET":
        m = m._repr_html_()

        context = {
            'm': m,
            'addCity': addCity(),

        }
        return render(request, 'sistema.html', context)
    else:
        flight.actualizar(request.POST["City"])

        m = m._repr_html_()

        context = {
            'm': m,
            'addCity': addCity(),

        }
        return render(request, 'sistema.html', context)
