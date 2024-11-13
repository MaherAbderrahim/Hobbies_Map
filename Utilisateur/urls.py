from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),       # Register new user
    path('login/', views.login_view, name='login'),           # Login
    path('logout/', views.logout_view, name='logout'),        # Logout
    path('users/', views.user_list, name='user_list'),        # List all users
    path('users/update/<int:pk>/', views.update_user, name='update_user'),  # Update user details
    path('users/delete/<int:pk>/', views.delete_user, name='delete_user'),  # Delete a user
    path('', views.homepage_view, name='homepage'),
]
