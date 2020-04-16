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

    def get_queryset(self):
        filtro = self.request.GET.get('filtro', '')
        if filtro == '':
            queryset = Documento.objects.all().order_by('iddocumento')
        else:
            queryset = Documento.objects.all().order_by('iddocumento').filter(Q(descripcion__icontains = filtro) | Q(nro__icontains = filtro)| Q(tipo__icontains = filtro))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListaDocumentos, self).get_context_data(**kwargs)
        context['filtro'] = self.request.GET.get('filtro', '')
        return context

class DetallesDocumento(DetailView):
    model = Documento
    template_name = 'documentos_detalle.html'

class AgregarDocumento(CreateView):
    model= Documento
    form_class= DocumentoForm
    template_name='documentos_agrega.html'
    success_url= reverse_lazy('documentos:documentoLista')

class EditarDocumento(UpdateView):
    model= Documento
    form_class = DocumentoForm
    template_name = 'documentos_edita.html'
    success_url = reverse_lazy('documentos:documentoLista')

class EliminarDocumento(DeleteView):
    model = Documento
    template_name = 'documentos_elimina.html'
    success_url = reverse_lazy('documentos:documentoLista')