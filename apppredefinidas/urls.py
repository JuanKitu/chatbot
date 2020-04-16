from django.conf.urls import url, patterns
from django.contrib import admin
from apppredefinidas import views
from django.contrib.auth.decorators import login_required

urlpatterns =  patterns('',
    # url(r'^admin/', admin.site.urls),
    url(r'lista$', login_required(views.listaPredefinidas.as_view()), name = 'predefinidasLista'),
    url(r'edita/(?P<pk>\d+)$', login_required(views.editaPredefinidas.as_view()), name = 'predefinidasEdita'),
    url(r'elimina/(?P<pk>\d+)$', login_required(views.eliminaPredefinidas.as_view()), name = 'predefinidasElimina'),
    url(r'agrega$', login_required(views.agregaPredefinidas.as_view()), name = 'predefinidasAgrega'),
                        )
