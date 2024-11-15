from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),       # Register new user
    path('login/', views.login_view, name='login'),  # 
    path('logout/', views.logout_view, name='logout'),        # Logout
    path('users/', views.user_list, name='user_list'),        # List all users
    path('users/update/<int:pk>/', views.update_user, name='update_user'),  # Update user details
    path('users/delete/<int:pk>/', views.delete_user, name='delete_user'),  # Delete a user
    path('', views.index_view, name='index'),  
    path('about/', TemplateView.as_view(template_name='user/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('pricing/', TemplateView.as_view(template_name='pricing.html'), name='pricing'),
    path('services/', TemplateView.as_view(template_name='services.html'), name='services'),
    path('home/', TemplateView.as_view(template_name='user/home.html'), name='home'),
    path('feedback',  TemplateView.as_view(template_name='user/feedback.html'),  name='feedback'),
    
]
