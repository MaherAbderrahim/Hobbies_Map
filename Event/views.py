from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Event, User_Event
from .forms import EventForm
from django.db.models import Q  # For complex queries
from .api_groq import ameliorer_description,generer_image  # Assurez-vous d'importer votre fonction
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@login_required
def event_list(request):
    # Get query parameters
    search_query = request.GET.get('q', '')  # Search keyword
    date_filter = request.GET.get('date', '')  # Filter by date
    price_min = request.GET.get('price_min', '')  # Minimum price
    price_max = request.GET.get('price_max', '')  # Maximum price

    # Start with all events
    events = Event.objects.all()

    # Apply filters
    if search_query:
        events = events.filter(
            Q(nom_event__icontains=search_query) | 
            Q(data__icontains=search_query)
        )
    if date_filter:
        events = events.filter(date_event__date=date_filter)  # Filter by exact date
    if price_min:
        events = events.filter(prix__gte=price_min)  # Price greater than or equal to
    if price_max:
        events = events.filter(prix__lte=price_max)  # Price less than or equal to

    return render(request, 'event/event_list.html', {'events': events})


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

@csrf_exempt  # Permet à cette vue d'accepter des requêtes POST sans vérification CSRF
def generate_image(request):
    """
    Vue Django pour générer et retourner une image basée sur une description.
    """
    print("je suis dans la vue generate_image")
    if request.method == 'POST':
        # Récupérer les données envoyées dans la requête
        data = json.loads(request.body)
        print("data = ",data)

        
        if not data:
            return JsonResponse({'error': "Le champ 'description' est requis"}, status=400)
        
        # Appeler la fonction pour générer une image
        image_url = generer_image(data)
        
        if image_url:
            return JsonResponse({'image_url': image_url})
        else:
            return JsonResponse({'error': "La génération ou l'upload de l'image a échoué"}, status=500)

    return JsonResponse({'error': 'Requête invalide'}, status=400)

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event/event_form.html', {'form': form})




from django.shortcuts import render, get_object_or_404
from .models import Event
from .forms import EventForm

def event_update(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')  # Or another URL to redirect after update
    else:
        form = EventForm(instance=event)
    return render(request, 'event/event_form.html', {'form': form, 'event': event})

@login_required
def event_delete(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'event/event_delete.html', {'event': event})

@login_required
def event_detail(request, id):
    event = get_object_or_404(Event, id=id)  # Retrieve the article with the specified ID
    return render(request, 'event/event_detail.html', {'event': event})
