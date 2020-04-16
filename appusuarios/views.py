from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from appusuarios.forms import RegistroForm

# Create your views here.
class RegistroUsuario(CreateView):
    model = User
    template_name = "registrar.html"
    form_class = RegistroForm
    success_url = '../accounts/login/'#reverse_lazy('')

    #print(success_url)

