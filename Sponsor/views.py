from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Sponsor
from .forms import SponsorForm

# Liste des sponsors
def sponsor_list(request):
    sponsors = Sponsor.objects.all()
    return render(request, 'Sponsor/spons_list.html', {'sponsors': sponsors})

# Détail d'un sponsor
def sponsor_detail(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    return render(request, 'Sponsor/spons_details.html', {'sponsor': sponsor})

# Création d'un sponsor
def sponsor_create(request):
    if request.method == 'POST':
        form = SponsorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = SponsorForm()
    return render(request, 'Sponsor/spons_form.html', {'form': form})

# Modification d'un sponsor
def sponsor_update(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    if request.method == 'POST':
        form = SponsorForm(request.POST, instance=sponsor)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = SponsorForm(instance=sponsor)
    return render(request, 'Sponsor/spons_form.html', {'form': form})

# Suppression d'un sponsor
def sponsor_delete(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    if request.method == 'POST':
        sponsor.delete()
        return redirect('list')
    return render(request, 'Sponsor/spons_delete.html', {'sponsor': sponsor})
