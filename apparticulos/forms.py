from django import forms
from apparticulos.models import Articulo

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = [
            'iddocumento',
            'tipo',
            'capitulo',
            'numero',
            'texto',
            ]
        labels = {
            'iddocumento':'IdDocumento',
            'tipo':'Tipo',
            'capitulo':'Capitulo',
            'numero':'Numero',
            'texto':'Texto',
            }
        widgets = {
            'iddocumento':forms.TextInput(attrs = {"class":"form-control", "readonly":"readonly"}),
            'tipo': forms.Select(),
            'capitulo':forms.TextInput(attrs = {"class":"form-control", "autofocus":"autofocus"}),
            'numero':forms.TextInput(attrs={"class":"form-control"}),
            'texto':forms.TextInput(attrs = {"class":"form-control"}),
            }