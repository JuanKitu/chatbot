from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apparticulos.models import Articulo
from apparticulos.forms import ArticuloForm
from django.db.models import Q

class listaArticulos(ListView):
    model = Articulo
    template_name = 'articulo_lista.html'
    paginate_by = 15

    def get_queryset(self):
        filtro = self.request.GET.get('filtro', '')
        if filtro == '':
            queryset = Articulo.objects.all().order_by('idarticulo')
        else:
            queryset = Articulo.objects.all().order_by('idarticulo').filter(Q(idarticulo__icontains = filtro) | Q(tipo__icontains = filtro)| Q(capitulo__icontains = filtro)| Q(numero__icontains = filtro)| Q(texto__icontains = filtro))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(listaArticulos, self).get_context_data(**kwargs)
        context['filtro'] = self.request.GET.get('filtro', '')
        return context

    # queryset = Sinonimo.objects.all().filter(palabra = filtro)
class listaArticulosUnDoc(ListView):
    #model = Articulo con request o contex
    template_name = 'articulo_lista1Documento.html'
    paginate_by = 15
    def get_queryset(self):
        iddoc = self.request.GET.get('id',None)
        filtro = self.request.GET.get('filtro', '')
        if filtro == '':
            queryset = Articulo.objects.order_by('iddocumento_id').filter(iddocumento_id=iddoc)
        else:
            queryset = Articulo.objects.all().order_by('idarticulo').filter(iddocumento_id=iddoc).filter(Q(idarticulo__icontains = filtro) | Q(tipo__icontains = filtro)| Q(capitulo__icontains = filtro)| Q(numero__icontains = filtro)| Q(texto__icontains = filtro))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(listaArticulosUnDoc, self).get_context_data(**kwargs)
        context['filtro'] = self.request.GET.get('filtro', '')
        context['id']=self.request.GET.get('id',None)
        return context

    # queryset = Sinonimo.objects.all().filter(palabra = filtro)

class editaArticulos(UpdateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'articulo_edita.html'
    success_url = reverse_lazy('articulos:articulosLista')

class agregaArticulos(CreateView):
    model = Articulo

    #Articulo.objects.filter(iddocumento_id=iddoc)
    #iddoc = self.request.GET.get('id', None)
    form_class = ArticuloForm
    template_name = 'articulo_agrega.html'
    success_url = reverse_lazy('articulos:articulosLista')
    iddoc=0
    def get_initial(self):
        inicial=super().get_initial()
        #self.object.iddocumento=1
        inicial['iddocumento']=self.request.GET.get('iddoc', None)
        return inicial
        #self.iddoc = self.request.GET.get('iddoc', None)

class eliminaArticulos(DeleteView):
    model = Articulo
    template_name = 'articulo_elimina.html'
    success_url = reverse_lazy('articulo:articulosLista')
