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
from appsinonimos import views
from django.contrib.auth.decorators import login_required
urlpatterns =  patterns('',
    # url(r'^admin/', admin.site.urls),
    url(r'lista$', login_required(views.listaSinonimos.as_view()), name = 'sinonimosLista'),
    url(r'edita/(?P<pk>\d+)$', login_required(views.editaSinonimos.as_view()), name = 'sinonimosEdita'),
    url(r'elimina/(?P<pk>\d+)$', login_required(views.eliminaSinonimos.as_view()), name = 'sinonimosElimina'),
    url(r'agrega$', login_required(views.agregaSinonimos.as_view()), name = 'sinonimosAgrega'),
                        )
