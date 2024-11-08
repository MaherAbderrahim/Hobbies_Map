from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),  # Liste des événements
    path('create/', views.event_create, name='event_create'),  # Ajouter un événement
    path('<int:id>/', views.event_detail, name='event_detail'),  # Détails d'un événement
    path('<int:id>/update/', views.event_update, name='event_update'),  # Modifier un événement
    path('<int:id>/delete/', views.event_delete, name='event_delete'),  # Supprimer un événement
]
