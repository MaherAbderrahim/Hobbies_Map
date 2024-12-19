from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomPasswordResetView
from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('classify/', views.find_user_view, name='classify'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('users/update/<int:pk>/', views.update_user, name='update_user'),
    path('users/delete/<int:pk>/', views.delete_user, name='delete_user'),
    path('about/', TemplateView.as_view(template_name='user/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('pricing/', TemplateView.as_view(template_name='pricing.html'), name='pricing'),
    path('services/', TemplateView.as_view(template_name='services.html'), name='services'),
    path('', TemplateView.as_view(template_name='user/home.html'), name='home'),
    path('feedback', TemplateView.as_view(template_name='user/feedback.html'), name='feedback'),
    path('face_recognition', TemplateView.as_view(template_name='user/face_recognition.html'), name='face_recognition'),
    path('password_reset/', views.CustomPasswordResetView.as_view(
        template_name='user/password_reset_form.html', 
        success_url='../password_reset_done/'), 
        name='password_reset'
    ),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html',success_url=reverse_lazy('user:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('favourites/', views.favourite_list, name='favourite_list'),
    path('favourite/add/<int:id>/', views.favourite_add, name='favourite_add'),
]

