from django.shortcuts import render
from django.views import generic

# Create your views here.

from catalogo.models import Genero, Linguagem, Autor, Livro, ExemplarLivro

def index(request):

    # Contando o número de livros e exemplares:
    num_livros = Livro.objects.all().count()
    num_exemplares = ExemplarLivro.objects.all().count()

    # Contando a quantidade de exemplares disponíveis (situacao = 'd')
    num_exemplares_disponiveis = ExemplarLivro.objects.filter(situacao__exact='d').count()

    # Contando o número de autores. A opção 'all()' é implícita por padrão:
    num_autores = Autor.objects.count()

    num_visitas = request.session.get('num_visitas', 1)
    request.session['num_visitas'] = num_visitas + 1

    contexto = {
        'num_livros': num_livros,
        'num_exemplares': num_exemplares,
        'num_exemplares_disponiveis': num_exemplares_disponiveis,
        'num_autores': num_autores,
        'num_visitas': num_visitas
    }

    # Renderizando o template index.html com os dados da variável contexto:
    return render(request, 'index.html', context=contexto)


class BookListView(generic.ListView):

    model = Livro


class BookDetailView(generic.DetailView):

    model = Livro


from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):

    model = ExemplarLivro
    template_name = 'catalogo/exemplares_emprestados_usuario.html'

    def get_queryset(self):
        return ExemplarLivro.objects.filter(usuario=self.request.user).filter(situacao__exact='e').order_by('data_devolucao')


import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required

from catalogo.forms import RenovarLivroForm


@permission_required('catalogo.pode_renovar_emprestimo')
def renew_book(request, pk):

    book_instance = get_object_or_404(ExemplarLivro, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenovarLivroForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.data_devolucao = form.cleaned_data['data_renovacao']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('meus-emprestimos') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenovarLivroForm(initial={'data_renovacao': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalogo/renovar_livro.html', context)

class AutorListView(generic.ListView):

    model = Autor


class AutorDetailView(generic.DetailView):

    model = Autor


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import PermissionRequiredMixin

class AutorCreate(PermissionRequiredMixin, CreateView):

    permission_required = 'catalogo.pode_manipular_autor'
    model = Autor
    fields = '__all__'
    initial = {'data_falecimento': '05/01/2018'}

class AutorUpdate(PermissionRequiredMixin, UpdateView):

    permission_required = 'catalogo.pode_manipular_autor'
    model = Autor
    fields = ['primeiro_nome', 'ultimo_nome', 'data_nascimento', 'data_falecimento']

class AutorDelete(PermissionRequiredMixin, DeleteView):

    permission_required = 'catalogo.pode_manipular_autor'
    model = Autor
    success_url = reverse_lazy('autores')
