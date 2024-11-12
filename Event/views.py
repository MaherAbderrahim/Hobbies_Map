from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, User_Event
from .forms import EventForm

# CRUD pour Event
def event_list(request):
    events = Event.objects.all()
    return render(request, 'event/event_list.html', {'events': events})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event/event_form.html', {'form': form})

# views.py
def event_update(request, id):  # Changed pk to id
    event = get_object_or_404(Event, id=id)  # Use id here instead of pk
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event/event_form.html', {'form': form})



# views.py
def event_delete(request, id):
    event = get_object_or_404(Event, id=id)
    
    # Check if the request method is POST (confirm deletion)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    
    # If it's a GET request, show the confirmation page
    return render(request, 'event/event_delete.html', {'event': event})


def event_detail(request, id):
    event = get_object_or_404(Event, id=id)  # Récupère l'article avec l'ID spécifié
    return render(request, 'event/event_detail.html', {'event': event})
