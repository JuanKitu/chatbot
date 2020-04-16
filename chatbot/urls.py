from django.conf.urls import patterns, include, url
from chatbot.views import *
from django.contrib.auth.views import login, logout_then_login
#from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',

    # Examples:
    # url(r'^$', 'chatbot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/login/', login,{'template_name':'index.html'}, name='login'),
    url(r'^logout/',logout_then_login, name='logout'),
    url(r'^sinonimos/', include('appsinonimos.urls', namespace='sinonimos')),
    url(r'^diccionario/', include('appdiccionario.urls', namespace='diccionario')),
    url(r'^keywords/', include('appkeywords.urls', namespace='keywords')),
    url(r'^predefinidas/', include('apppredefinidas.urls', namespace='predefinidas')),
    url(r'^documentos/', include('appdocumentos.urls', namespace='documentos')),
    url(r'^articulos/', include('apparticulos.urls', namespace='articulos')),
    url(r'^usuarios/', include('appusuarios.urls', namespace='usuarios')),
    url(r'^$', main, name='home'),

    url(r'^navbar',navbar),
    url(r'^processmessage/$', process_message),
    url(r'^contact/$', contact),
    url(r'^populate/$', populate_database),
    url(r'^contact/submit/', send_contact),
#    url(r'^documentos/lista$', ListaDocumentos.as_view(), name='listadocumentos'),
#    url(r'^documentos/detalle$', DetallesDocumento.as_view(), name='detalledocumento'),
)
