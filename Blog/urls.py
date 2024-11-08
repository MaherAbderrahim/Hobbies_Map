from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='list'),  # Liste des articles
    path('create/', views.post_create, name='form'),  # Ajouter un article
    path('<int:id>/', views.post_detail, name='detail'),  # Détails d'un article
    path('<int:id>/update/', views.post_update, name='form'),  # Modifier un article
    path('<int:id>/delete/', views.post_delete, name='delete'),  # Supprimer un article
]
