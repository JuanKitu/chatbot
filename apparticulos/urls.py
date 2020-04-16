"""sinonimos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns
from django.contrib import admin
from apparticulos import views
from django.contrib.auth.decorators import login_required

urlpatterns =  patterns('',
    # url(r'^admin/', admin.site.urls),
    url(r'lista$', login_required(views.listaArticulos.as_view()), name = 'articulosLista'),
    url(r'listadoc/$', login_required(views.listaArticulosUnDoc.as_view()), name = 'articulosListaunDocumento'),
    url(r'edita/(?P<pk>\d+)$', login_required(views.editaArticulos.as_view()), name = 'articulosEdita'),
    url(r'elimina/(?P<pk>\d+)$', login_required(views.eliminaArticulos.as_view()), name = 'articulosElimina'),
    url(r'agrega$', login_required(views.agregaArticulos.as_view()), name = 'articulosAgrega'),
                        )
