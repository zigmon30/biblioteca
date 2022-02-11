from django.urls import path
from catalogo import views

urlpatterns = [
    path('', views.index, name='index'),
    path('livros/', views.BookListView.as_view(), name='livros'),
    path('livros/<int:pk>', views.BookDetailView.as_view(), name='livro-detalhes'),
]

urlpatterns += [
    path('meusemprestimos/', views.LoanedBooksByUserListView.as_view(), name='meus-emprestimos'),
]

urlpatterns += [
    path('livro/<uuid:pk>/renovar/', views.renew_book, name='renovar-livro'),
]

urlpatterns += [
    path('autores/', views.AutorListView.as_view(), name='autores'),
    path('autores/<int:pk>', views.AutorDetailView.as_view(), name='autor-detalhes'),
    path('autor/create/', views.AutorCreate.as_view(), name='autor-create'),
    path('autor/<int:pk>/update/', views.AutorUpdate.as_view(), name='autor-update'),
    path('autor/<int:pk>/delete/', views.AutorDelete.as_view(), name='autor-delete'),
]
