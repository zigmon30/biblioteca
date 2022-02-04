from django.contrib import admin

from .models import Autor, Genero, Livro, ExemplarLivro, Linguagem


admin.site.register(Livro)
admin.site.register(Autor)
admin.site.register(ExemplarLivro)
admin.site.register(Genero)
admin.site.register(Linguagem)
