from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from appsinonimos.models import Sinonimo
from appsinonimos.forms import SinonimoForm
from django.db.models import Q

class listaSinonimos(ListView):
    model = Sinonimo
    template_name = 'sinonimo_lista.html'
    paginate_by = 15

    def get_queryset(self):
        filtro = self.request.GET.get('filtro', '')
        if filtro == '':
            queryset = Sinonimo.objects.all().order_by('palabra')
        else:
            queryset = Sinonimo.objects.all().order_by('palabra').filter(Q(palabra__icontains = filtro) | Q(sinonimo__icontains = filtro))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(listaSinonimos, self).get_context_data(**kwargs)
        context['filtro'] = self.request.GET.get('filtro', '')
        return context

    # queryset = Sinonimo.objects.all().filter(palabra = filtro)

class editaSinonimos(UpdateView):
    model = Sinonimo
    form_class = SinonimoForm
    template_name = 'sinonimo_edita.html'
    success_url = reverse_lazy('sinonimos:sinonimosLista')

class agregaSinonimos(CreateView):
    model = Sinonimo
    form_class = SinonimoForm
    template_name = 'sinonimo_agrega.html'
    success_url = reverse_lazy('sinonimos:sinonimosLista')

class eliminaSinonimos(DeleteView):
    model = Sinonimo
    template_name = 'sinonimo_elimina.html'
    success_url = reverse_lazy('sinonimos:sinonimosLista')
