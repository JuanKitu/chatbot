from django.shortcuts import render
from appdocumentos.models import Documento
from appdocumentos.forms import DocumentoForm
from django.db.models import Q
from django.views.generic import CreateView, ListView, DetailView,UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

# Create your views here.
class ListaDocumentos(ListView):
    model = Documento
    template_name = 'documentos_lista.html'
    paginate_by = 15
    queryset = Documento.objects.all().order_by('iddocumento')  # Default: Model.objects.all()

class DetallesDocumento(DetailView):
    model = Documento

class AgregarDocumento(CreateView):
    model= Documento
    form_class= DocumentoForm
    template_name='documentos_agrega.html'
    success_url= reverse_lazy('documentos:documentosLista')

class EditarDocumento(UpdateView):
    model= Documento
    form_class = DocumentoForm
    template_name = 'documentos_edita.html'
    success_url = reverse_lazy('documentos:documentosLista')

class EliminarDocumento(DeleteView):
    model = Documento
    template_name = 'documentos_elimina.html'
    success_url = reverse_lazy('documentos:documentosLista')