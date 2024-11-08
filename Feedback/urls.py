from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_list, name='feedback_list'),  # Liste des feedbacks
    path('create/', views.feedback_create, name='feedback_create'),  # Ajouter un feedback
    path('<int:id>/', views.feedback_detail, name='feedback_detail'),  # Détails d'un feedback
    path('<int:id>/update/', views.feedback_update, name='feedback_update'),  # Modifier un feedback
    path('<int:id>/delete/', views.feedback_delete, name='feedback_delete'),  # Supprimer un feedback
]
