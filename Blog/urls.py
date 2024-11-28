from django.urls import path
from . import views
from .views import  *

urlpatterns = [
    path('', list , ),
    path('details/<int:ide>', detailsPoste , name="details"),
    
    path('listclass/', ListPoste.as_view() , name="list"),
    
    path('detailsclass/<int:pk>', Details.as_view() , name="detailsClass"),
    path('add/', AddPoste.as_view() , name="add"),
    path('updateclass/<int:pk>', UpdatePoste.as_view() , name="updateClass"),
    path('deleteclass/<int:pk>', DeletePoste.as_view() , name="deleteClass"),
    

    path('notifications/', notifications, name='notifications'),
    
    
    path('like/<int:post_id>/', toggle_like, name='toggle_like'),

]
