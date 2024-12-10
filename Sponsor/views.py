from io import BytesIO
import qrcode
import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Sponsor
from .forms import SponsorForm
from .api_groq import ameliorer_description  # Assurez-vous d'importer votre fonction
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


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


@csrf_exempt  # Assurez-vous que cette vue peut accepter des requêtes POST
def improve_description(request):
    if request.method == 'POST':
        # Récupérer la description envoyée
        data = json.loads(request.body)
        description_utilisateur = data.get('description')

        # Appeler votre fonction d'amélioration de la description ici
        improved_description = ameliorer_description(description_utilisateur)  # La fonction pour améliorer la description
        
        # Retourner la description améliorée en JSON
        return JsonResponse({'improved_description': improved_description})

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Création d'un sponsor
@superuser_required
def sponsor_create(request):
    chat_response = ''
    if request.method == 'POST':
        form = SponsorForm(request.POST)
        
        # Si l'utilisateur demande à améliorer la description
        if 'improve_description' in request.POST:
            description = request.POST.get('description_sponsor', '')  # Obtenez la description du formulaire
            if description:
                chat_response = ameliorer_description(description)  # Appeler la fonction pour améliorer la description

        if form.is_valid():
            sponsor = form.save()  # Sauvegarder le sponsor

            # Si une réponse de l'API est générée, la mettre à jour
            if chat_response:
                sponsor.description_sponsor = chat_response
                sponsor.save()

            return redirect('spons_list')
    else:
        form = SponsorForm()

    return render(request, 'Sponsor/spons_form.html', {
        'form': form,
        'chat_response': chat_response,  # Passer la réponse à votre template
    })


# Modification d'un sponsor
@superuser_required
def sponsor_update(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    chat_response = ''
    
    if request.method == 'POST':
        form = SponsorForm(request.POST, instance=sponsor)
        
        # Si l'utilisateur demande à améliorer la description
        if 'improve_description' in request.POST:
            description = request.POST.get('description_sponsor', '')  # Obtenez la description du formulaire
            if description:
                chat_response = ameliorer_description(description)  # Appeler la fonction pour améliorer la description

        if form.is_valid():
            form.save()  # Sauvegarder les modifications du sponsor

            # Si une réponse de l'API est générée, la mettre à jour
            if chat_response:
                sponsor.description_sponsor = chat_response
                sponsor.save()

            return redirect('spons_list')
    else:
        form = SponsorForm(instance=sponsor)

    return render(request, 'Sponsor/spons_form.html', {
        'form': form,
        'chat_response': chat_response,  # Passer la réponse à votre template
    })



# Suppression d'un sponsor
@superuser_required
def sponsor_delete(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    if request.method == 'POST':
        sponsor.delete()
        return redirect('spons_list')
    return render(request, 'Sponsor/spons_delete.html', {'sponsor': sponsor})


