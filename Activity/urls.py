from django.urls import path
from . import views
# In Activity/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ActivityListView.as_view(), name='act_list'),
    path('add/', views.ActivityCreateView.as_view(), name='act_form'),
    path('<int:pk>/edit/', views.ActivityUpdateView.as_view(), name='act_form'),
    path('<int:pk>/delete/', views.ActivityDeleteView.as_view(), name='act_delete'),
    path('<int:pk>/', views.ActivityDetailView.as_view(), name='act_detail'),
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
]
