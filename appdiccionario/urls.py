from django.conf.urls import url, patterns
from chatbot.views import *
from appdiccionario.views import Listadiccionario
from appdiccionario.views import Editardiccionario
from appdiccionario.views import Eliminardiccionario
from appdiccionario.views import Agregardiccionario
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',

    # Examples:
    # url(r'^$', 'chatbot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'lista$',login_required(Listadiccionario.as_view()),name='Diccionariolista'),
    url(r'editar/(?P<pk>\d+)$',login_required(Editardiccionario.as_view()), name='Diccionarioeditar'),
    url(r'eliminar/(?P<pk>\d+)$',login_required(Eliminardiccionario.as_view()), name='Diccionarioeliminar'),
    url(r'agregar$',login_required(Agregardiccionario.as_view()), name='Diccionarioagregar'),
                       )
