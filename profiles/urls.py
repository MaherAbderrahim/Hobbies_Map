from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    path('add_photo/', views.add_photo, name='add_photo'),
    path('modify_photo/', views.modify_photo, name='modify_photo'),
]
