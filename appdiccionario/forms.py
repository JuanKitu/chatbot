from django import forms
from appdiccionario.models import Diccionario

class DiccionarioForm(forms.ModelForm):
    class Meta:
        model=Diccionario
        fields=['palabra',
                'porter',]
        labels={'palabra':'Palabra',
                'porter':'Porter',}
        widgets={'palabra':forms.TextInput(attrs={'class':'form-control'}),
                 'porter':forms.TextInput(attrs={'class':'form-control'}),}
