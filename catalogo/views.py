from django.shortcuts import render
from django.views import generic

# Create your views here.

from catalogo.models import Livro, Autor, ExemplarLivro, Genero, Linguagem


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_livros = Livro.objects.all().count()
    num_exemplares = ExemplarLivro.objects.all().count()
    # Available copies of books
    num_exemplares_deisponiveis = ExemplarLivro.objects.filter(situacao='d').count()
    num_autores = Autor.objects.count()  # The 'all()' is implied by default.


    contexto = {
        'num_livros': num_livros,
        'num_exemplares': num_exemplares,
        'num_exemplares_deisponiveis': num_exemplares_deisponiveis,
        'num_autores': num_autores,
    }


    return render(request, 'index.html', context=contexto)

class BookListView(generic.ListView):
    model = Livro

class BookDetailView(generic.DetailView):
    model = Livro
