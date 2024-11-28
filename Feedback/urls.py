from django.urls import path
from . import views

app_name = 'feedback'  # Namespace is 'feedback'

urlpatterns = [
    path('', views.feedback_list, name='feedback'),  # Root URL for the feedback list
    path('create/', views.feedback_create, name='feedback_create'),
    path('update/<int:feedback_id>/', views.feedback_update, name='feedback_update'),  
    path('delete/<int:feedback_id>/', views.feedback_delete, name='feedback_delete'),
]
