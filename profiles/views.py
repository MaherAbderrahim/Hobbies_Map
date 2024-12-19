from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'user/profile.html', {'profile': profile})

@login_required
def add_photo(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST' and request.FILES.get('photo'):
        profile.photo = request.FILES['photo']
        profile.save()
        return redirect('profile_view')
    return render(request, 'user/profile.html', {'profile': profile})

@login_required
def modify_photo(request):
    return add_photo(request)  # Same logic as adding
