from django import forms
from appdocumentos.models import Documento
import datetime
class DocumentoForm(forms.ModelForm):
    class Meta:
        model=Documento
       #fields es campos a poner en el formulario
        fields=[
            'nro',
            'fecha',
            'descripcion',
            'tipo',
            'texto',
        ]
        #Labels van a ser las etiquetas que va a tomar ese campo
        labels=[{
            'nro':'Numero De Documento',
            'fecha':'Fechaaaaa',
            'descripcion':'Titulo',
            'tipo':'Tipo',
            'texto':'Texto',
            }]
        #el formato de las cajas de texto
        widgets=[{
            'nro':forms.TextInput(attrs = {"class":"form-control"}),
            'fecha':forms.DateField(widget=forms.widgets.DateInput(format='%d/%m/%y')),
            'descripcion':forms.TextInput(attrs = {"class":"form-control"}),
            'tipo':forms.ChoiceField(),
            'texto':forms.TextInput(attrs = {"class":"form-control"}),
        }]