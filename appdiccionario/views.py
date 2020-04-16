from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from appdiccionario.models import Diccionario
from appdiccionario.forms import DiccionarioForm
from django.views.generic import CreateView, ListView,UpdateView, DeleteView
from django.db.models import Q

class Listadiccionario(ListView):
    model = Diccionario
    template_name = 'diccionario_lista.html'
    paginate_by = 15

    def get_queryset(self):
        filtro = self.request.GET.get('filtro', '')
        if filtro == '':
            queryset = Diccionario.objects.all().order_by('palabra')
        else:
            queryset = Diccionario.objects.all().order_by('palabra').filter(Q(palabra__icontains = filtro) | Q(porter__icontains = filtro))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(Listadiccionario, self).get_context_data(**kwargs)
        context['filtro'] = self.request.GET.get('filtro', '')
        return context

    # queryset = Sinonimo.objects.all().filter(palabra = filtro)

class Editardiccionario(UpdateView):
    model = Diccionario
    form_class = DiccionarioForm
    template_name = 'diccionario_edita.html'
    success_url = reverse_lazy('diccionario:Diccionariolista')

class Agregardiccionario(CreateView):
    model = Diccionario
    form_class = DiccionarioForm
    template_name = 'diccionario_agrega.html'
    success_url = reverse_lazy('diccionario:Diccionariolista')

class Eliminardiccionario(DeleteView):
    model = Diccionario
    template_name = 'diccionario_elimina.html'
    success_url = reverse_lazy('diccionario:Diccionariolista')