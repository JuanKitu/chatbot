from django import forms
from apppredefinidas.models import Predefinida

class PredefinidaForm(forms.ModelForm):
    class Meta:
        model = Predefinida
        fields = [
            'question',
            'expression',
            'reglamento',
            'articulo',
            ]
        labels = {
            'question':'Pregunta',
            'expression':'Patron',
            'reglamento':'Reglamento',
            'articulo':'id Articulo',
            }
        widgets = {
            #'id':forms.TextInput(attrs = {"class":"form-control-static readonly"}),
            'question':forms.TextInput(attrs = {"class":"form-control"}),
            'expression':forms.TextInput(attrs = {"class":"form-control"}),
            'reglamento':forms.TextInput(attrs = {"class":"form-control"}),
            'articulo':forms.NumberInput(attrs = {"class":"form-control"}),
            }