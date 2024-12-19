from django.urls import path
from . import views

# urls.py
urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_form'),
    path('<int:id>/', views.event_detail, name='event_detail'),
    path('<int:id>/update/', views.event_update, name='event_update'),  
    path('<int:id>/delete/', views.event_delete, name='event_delete'),
    path('generate-image/', views.generate_image, name='generate_image'),

]

