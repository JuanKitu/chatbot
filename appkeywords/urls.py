from django.conf.urls import url, patterns
from django.contrib import admin
from appkeywords import views
from chatbot.views import *
from django.contrib.auth.decorators import login_required

urlpatterns =  patterns('',
    # url(r'^admin/', admin.site.urls),
    url(r'lista$', login_required(views.ListaKeywords.as_view()), name = 'keywordsLista'),
    url(r'edita/(?P<pk>\d+)$', login_required(views.EditaKeywords.as_view()), name = 'keywordsEdita'),
    url(r'elimina/(?P<pk>\d+)$', login_required(views.EliminaKeywords.as_view()), name = 'keywordsElimina'),
    url(r'agrega$', login_required(views.AgregaKeywords.as_view()), name = 'keywordsAgrega'),
                        )