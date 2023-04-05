from django.shortcuts import render
from django.http import HttpResponse
import folium
# Create your views here.

def index(request):
    return render(request, 'index.html', {})
def mapa(request):
    m = folium.Map()
    m = m._repr_html_()
    context = {
        'm' : m,
    }
    return render(request, 'sistema.html',context)