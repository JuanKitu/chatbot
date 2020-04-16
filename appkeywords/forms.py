from django import forms
from appkeywords.models import Keyword

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = [
            'palabra',
            'stem',
            ]
        labels = {
            'palabra':'Palabra',
            'stem':'Stem',
            }
        widgets = {
            #'id':forms.TextInput(attrs = {"class":"form-control-static readonly"}),
            'palabra':forms.TextInput(attrs = {"class":"form-control"}),
            'stem':forms.TextInput(attrs = {"class":"form-control"}),
            }