from django import forms
from appdocumentos.models import Documento
import datetime
class DocumentoForm(forms.ModelForm):
    class Meta:
        model=Documento
       #fields es campos a poner en el formulario
        fields=[
            'nro',
            'tipo',
            'fecha',
            'descripcion',
            'texto',
        ]
        #Labels van a ser las etiquetas que va a tomar ese campo
        labels=[{
            'nro':'Numero De Documento',
            'tipo': 'Tipo',
            'fecha':'Fecha',
            'descripcion':'Titulo',
            'texto':'Texto',
            }]
        #el formato de las cajas de texto
        widgets=[{
            'nro':forms.TextInput(attrs = {'class':'form-control'}),
            'fecha':forms.DateField(widget=forms.DateInput(format=('%d/%m/%y'),attrs={'placeholder':'2000-12-30'})),
            'descripcion':forms.TextInput(attrs = {'class':'form-control'}),
            'tipo':forms.Select(),
            'texto':forms.TextInput(attrs = {'class':'form-control'}),
        }]