from django.conf.urls import patterns, url
from appdocumentos import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',

    # Examples:
    # url(r'^$', 'chatbot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^lista$', login_required(views.ListaDocumentos.as_view()), name='documentoLista'),
    url(r'^detalle/(?P<pk>\d+)$', login_required(views.DetallesDocumento.as_view()), name='documentoDetalle'),
    url(r'agregar$', login_required(views.AgregarDocumento.as_view()),name='DocumentoAgrega'),
    url(r'editar/(?P<pk>\d+)$', login_required(views.EditarDocumento.as_view()),name='DocumentoEdita'),
    url(r'eliminar/(?P<pk>\d+)$', login_required(views.EliminarDocumento.as_view()),name='DocumentoElimina'),
)
