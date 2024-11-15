# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('feedbacks/', views.feedback_list, name='feedback_list'),
    path('feedbacks/create/', views.feedback_create, name='feedback_create'),
    path('feedbacks/update/<int:feedback_id>/', views.feedback_update, name='feedback_update'),
    path('feedbacks/delete/<int:feedback_id>/', views.feedback_delete, name='feedback_delete'),
]
