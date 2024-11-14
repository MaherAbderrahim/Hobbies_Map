from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from .models import Sponsor
from .forms import SponsorForm

# Décorateur pour vérifier si l'utilisateur est un superuser
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

# Liste des sponsors
@superuser_required
def sponsor_list(request):
    print(f"Utilisateur connecté : {request.user}")  # Affiche l'utilisateur connecté dans la console
    sponsors = Sponsor.objects.all()
    return render(request, 'Sponsor/spons_list.html', {'sponsors': sponsors})

# Détail d'un sponsor
@superuser_required
def sponsor_detail(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    return render(request, 'Sponsor/spons_details.html', {'sponsor': sponsor})

# Création d'un sponsor
@superuser_required
def sponsor_create(request):
    if request.method == 'POST':
        form = SponsorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('spons_list')
    else:
        form = SponsorForm()
    return render(request, 'Sponsor/spons_form.html', {'form': form})

# Modification d'un sponsor
@superuser_required
def sponsor_update(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    if request.method == 'POST':
        form = SponsorForm(request.POST, instance=sponsor)
        if form.is_valid():
            form.save()
            return redirect('spons_list')
    else:
        form = SponsorForm(instance=sponsor)
    return render(request, 'Sponsor/spons_form.html', {'form': form})

# Suppression d'un sponsor
@superuser_required
def sponsor_delete(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    if request.method == 'POST':
        sponsor.delete()
        return redirect('spons_list')
    return render(request, 'Sponsor/spons_delete.html', {'sponsor': sponsor})
