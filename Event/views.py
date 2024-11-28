from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required  # Import the decorator
from .models import Event, User_Event
from .forms import EventForm
from django.db.models import Q  # For complex queries

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
            Q(description_event__icontains=search_query)
        )
    if date_filter:
        events = events.filter(date_event__date=date_filter)  # Filter by exact date
    if price_min:
        events = events.filter(prix__gte=price_min)  # Price greater than or equal to
    if price_max:
        events = events.filter(prix__lte=price_max)  # Price less than or equal to

    return render(request, 'event/event_list.html', {'events': events})

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
