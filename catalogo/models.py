from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns


class Genero(models.Model):
    nome = models.CharField(max_length=200, help_text="Entre com um genero do livro (ex Ficção Cientifica.)"
        )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.nome


class Linguagem(models.Model):
    nome = models.CharField(max_length=200, help_text="Enttre com a Linguagem do livro(ex: Portugues, Ingles, Frances, etc...)")

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    resumo = models.TextField(max_length=1000, help_text="Entre com uma descrição do livro")
    isbn = models.CharField('ISBN', max_length=13)
    genero = models.ManyToManyField('Genero', help_text="Selecione um genero para o livro")
    linguagem = models.ForeignKey('Linguagem', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['titulo', 'autor']

    def __str__(self):
        return self.titulo


import uuid

from django.contrib.auth.models import User  # Required to assign User as a borrower


class ExemplarLivro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="identificador unico para exemplar")
    livro = models.ForeignKey(Livro, on_delete=models.SET_NULL, null=True)
    editoto = models.CharField(max_length=200)
    data_devolucao = models.DateField(null=True, blank=True)

    SITUACAO_EXEMPLAR = (
        ('m', 'Manutencao'),
        ('e', 'Emprestado'),
        ('d', 'Disponivel'),
        ('r', 'Reservado'),
    )

    situacao = models.CharField(
        max_length=1,
        choices=SITUACAO_EXEMPLAR,
        blank=True,
        default='m',
        help_text='situacao do exemplar'
    )

    class Meta:
        ordering = ['data_devolucao']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}, {self.livro.titulo}'


class Autor(models.Model):

    primeiro_nome = models.CharField(max_length=100)
    ultimo_nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    data_falecimento = models.DateField('morte', null=True, blank=True)

    class Meta:
        ordering = ['ultimo_nome', 'primeiro_nome']

    def __str__(self):
        return f'{self.ultimo_nome}, {self.primeiro_nome}'