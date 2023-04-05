from django.shortcuts import render
from django.http import HttpResponse
import folium
from API.codigodeapiOOP import FlightMap
# Create 
# your views here.

def index(request):
    return render(request, 'index.html', {})
def mapa(request):
    flight = FlightMap()
    m = flight.create_map()
    m = m._repr_html_()
    context = {
        'm' : m,
    }
    return render(request, 'sistema.html',context)