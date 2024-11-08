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

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event/event_form.html', {'form': form})



def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('event_list')

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)  # Récupère l'article avec l'ID spécifié
    return render(request, 'event/event_detail.html', {'event': event})
