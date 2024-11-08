from django.urls import path
from . import views

urlpatterns = [
    path('', views.ActivityListView.as_view(), name='act_list'),
    path('add/', views.ActivityCreateView.as_view(), name='act_form'),
    path('edit/<int:pk>/', views.ActivityUpdateView.as_view(), name='act_form'),
    path('delete/<int:pk>/', views.ActivityDeleteView.as_view(), name='act_delete'),

    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('categories/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
]
