from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apppredefinidas.models import Predefinida
from apppredefinidas.forms import PredefinidaForm
from django.db.models import Q

class listaPredefinidas(ListView):
    model = Predefinida
    template_name = 'predefinida_lista.html'
    paginate_by = 15

    def get_queryset(self):
        filtro = self.request.GET.get('filtro', '')
        if filtro == '':
            queryset = Predefinida.objects.all().order_by('id')
        else:
            queryset = Predefinida.objects.all().order_by('id').filter(Q(question__icontains = filtro) | Q(expression__icontains = filtro))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(listaPredefinidas, self).get_context_data(**kwargs)
        context['filtro'] = self.request.GET.get('filtro', '')
        return context

    # queryset = Sinonimo.objects.all().filter(palabra = filtro)

class editaPredefinidas(UpdateView):
    model = Predefinida
    form_class = PredefinidaForm
    template_name = 'predefinida_edita.html'
    success_url = reverse_lazy('predefinidas:predefinidasLista')

class agregaPredefinidas(CreateView):
    model = Predefinida
    form_class = PredefinidaForm
    template_name = 'predefinida_agrega.html'
    success_url = reverse_lazy('predefinidas:predefinidasLista')

class eliminaPredefinidas(DeleteView):
    model = Predefinida
    template_name = 'predefinida_elimina.html'
    success_url = reverse_lazy('predefinidas:predefinidasLista')
