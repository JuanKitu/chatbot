from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from appkeywords.models import Keyword
from appkeywords.forms import KeywordForm
from django.db.models import Q

class ListaKeywords(ListView):
    model = Keyword
    template_name = 'Keyword_lista.html'
    paginate_by = 15

    def get_queryset(self):
        filtro = self.request.GET.get('filtro', '')
        if filtro == '':
            queryset = Keyword.objects.all().order_by('palabra')
        else:
            queryset = Keyword.objects.all().order_by('palabra').filter(Q(palabra__icontains = filtro) | Q(stem__icontains = filtro))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListaKeywords, self).get_context_data(**kwargs)
        context['filtro'] = self.request.GET.get('filtro', '')
        return context

    # queryset = Keyword.objects.all().filter(palabra = filtro)

class EditaKeywords(UpdateView):
    model = Keyword
    form_class = KeywordForm
    template_name = 'Keyword_edita.html'
    success_url = reverse_lazy('keywords:keywordsLista')

class AgregaKeywords(CreateView):
    model = Keyword
    form_class = KeywordForm
    template_name = 'Keyword_agrega.html'
    success_url = reverse_lazy('keywords:keywordsLista')

class EliminaKeywords(DeleteView):
    model = Keyword
    template_name = 'Keyword_elimina.html'
    success_url = reverse_lazy('keywords:keywordsLista')