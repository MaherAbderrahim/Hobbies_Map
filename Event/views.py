from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required  # Import the decorator
from .models import Event, User_Event
from .forms import EventForm

# CRUD for Event
@login_required
def event_list(request):
    events = Event.objects.all()
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

@login_required
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
