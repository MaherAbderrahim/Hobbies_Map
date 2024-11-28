from io import BytesIO
import qrcode
import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Sponsor
from .forms import SponsorForm

# Décorateur pour vérifier si l'utilisateur est un superuser
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@superuser_required
def sponsor_list(request):
    print(f"Utilisateur connecté : {request.user}")  # Affiche l'utilisateur connecté dans la console

    # Récupérer les paramètres de recherche et de filtrage
    search_query = request.GET.get('search', '')
    price_filter = request.GET.get('price', '')

    # Filtrer les sponsors par nom
    sponsors = Sponsor.objects.all()
    if search_query:
        sponsors = sponsors.filter(nom_sponsor__icontains=search_query)

    # Filtrer les sponsors par prix (supérieur)
    if price_filter:
        try:
            price_value = float(price_filter)
            sponsors = sponsors.filter(prix_sponsor__gte=price_value)  # Filtre les sponsors dont le prix est supérieur ou égal à price_value
        except ValueError:
            pass  # Ignore si le filtre de prix n'est pas un nombre valide
    return render(request, 'Sponsor/spons_list.html', {'sponsors': sponsors, 'search_query': search_query, 'price_filter': price_filter})

from io import BytesIO  # Assurez-vous d'importer BytesIO

@superuser_required
def sponsor_detail(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)

    # Générer le QR code
    qr_data = sponsor.url_site
    qr_code_img = qrcode.make(qr_data)

    # Convertir le QR code en base64 pour l'afficher dans le template
    buffered = BytesIO()
    qr_code_img.save(buffered, format="PNG")
    qr_code_base64 = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

    return render(request, 'Sponsor/spons_details.html', {'sponsor': sponsor, 'qr_code_base64': qr_code_base64})

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


