from django.shortcuts import render


from django.views.generic import CreateView 
# Create your views here.

from django.contrib.auth.views import LoginView
from .forms import RegisterForm
from .models import Participant
from django.urls import reverse_lazy
from django.urls import reverse

class Register(CreateView):
    
    model=Participant
    
    form_class= RegisterForm
    template_name = "user/register.html"
    
    success_url = reverse_lazy('login')
    
    
    
class Login(LoginView):
    template_name="user/login.html"
    
    def get_success_url(self):
        return reverse('list')
