from django import forms
from appsinonimos.models import Sinonimo

class SinonimoForm(forms.ModelForm):
    class Meta:
        model = Sinonimo
        fields = [
            'palabra',
            'sinonimo',
            ]
        labels = {
            'palabra':'Palabra',
            'sinonimo':'Sinonimo',
            }
        widgets = {
            #'id':forms.TextInput(attrs = {"class":"form-control-static readonly"}),
            'palabra':forms.TextInput(attrs = {"class":"form-control"}),
            'sinonimo':forms.TextInput(attrs = {"class":"form-control"}),
            }