
from django.conf.urls import url, patterns
#from django.contrib import admin
from appusuarios import views
#from chatbot.views import *

urlpatterns =  patterns('',
    #url(r'^accounts/login/', loginApUsuario, {'template_name': 'index.html'}, name='login'),
    url(r'^registrar',views.RegistroUsuario.as_view(), name="usuarioRegistrar"),


                        )
