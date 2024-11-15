from django.urls import path
from . import views

urlpatterns = [
    path('', views.sponsor_list, name='spons_list'),  # Liste des sponsors
    path('create/', views.sponsor_create, name='spons_form'),  # Ajouter un sponsor
    path('<int:pk>/', views.sponsor_detail, name='spons_detail'),  # Détails d'un sponsor
    path('<int:pk>/update/', views.sponsor_update, name='spons_form'),  # Modifier un sponsor
    path('<int:pk>/delete/', views.sponsor_delete, name='spons_delete'),  # Supprimer un sponsor
]
