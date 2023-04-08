from django import forms

class addCity(forms.Form):
    City= forms.CharField(label="Ingrese la ciudad de origen", max_length=200, widget=forms.TextInput(attrs={"color":"black"}), required=False)
    destiny = forms.CharField(label="Ingrese la ciudad del destino",max_length=200, widget=forms.TextInput(attrs={"color":"black"}), required=False)
    bfs = forms.CharField(label="Ingrese la ciudad que quiere aplicar BFS",max_length=200, widget=forms.TextInput(attrs={"color":"black"}), required=False)