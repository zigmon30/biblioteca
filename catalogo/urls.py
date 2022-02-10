from django.urls import path
from catalogo import views

urlpatterns = [
path('', views.index, name='index'),
path('livros/', views.BookListView.as_view(), name='livros'),
path('livros/<int:pk>', views.BookDetailView.as_view(), name='livro-detalhes'),

]
