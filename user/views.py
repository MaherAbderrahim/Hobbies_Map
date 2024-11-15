from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Utilisateur
from .forms import UtilisateurCreationForm, UtilisateurLoginForm

# Register a new user
def register(request):
    if request.method == 'POST':
        form = UtilisateurCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('login')
        else:
            print("Form errors:", form.errors)  # Debugging
    else:
        form = UtilisateurCreationForm()
    return render(request, 'user/register.html', {'form': form})

from django.contrib.auth import login, authenticate
from .forms import UtilisateurLoginForm

def login_view(request):
    if request.method == 'POST':
        form = UtilisateurLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('user:home')  
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = UtilisateurLoginForm()
    return render(request, 'user/login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# List all users
@login_required
def user_list(request):
    users = Utilisateur.objects.all()
    return render(request, 'user/user_list.html', {'users': users})

# Update user details
@login_required
def update_user(request, pk):
    user = get_object_or_404(Utilisateur, pk=pk)
    if request.method == 'POST':
        form = UtilisateurCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UtilisateurCreationForm(instance=user)
    return render(request, 'user/user_form.html', {'form': form})

# Delete a user
@login_required
def delete_user(request, pk):
    user = get_object_or_404(Utilisateur, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user/user_confirm_delete.html', {'user': user})

def index_view(request):
    return render(request, 'user/index.html')


