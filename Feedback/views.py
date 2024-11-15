from django.shortcuts import render, redirect, get_object_or_404
from .models import Feedback
from .forms import FeedbackForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Utilisateur


# feedback/views.py

@login_required
def feedback_list(request):
    # Retrieve feedbacks for the logged-in user
    feedbacks = Feedback.objects.filter(utilisateur=request.user)
    print("Retrieved feedbacks:", feedbacks)  # Debugging line to ensure feedbacks are fetched correctly
    print("Current logged-in user:", request.user)
    
    return render(request, 'user/feedback.html', {'feedbacks': feedbacks})


@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.utilisateur = request.user  # Associate feedback with the logged-in user
            feedback.save()
            return redirect('feedback_list')  # Redirect to the list page

    else:
        form = FeedbackForm()

    return render(request, 'Feedback/feed_form.html', {'form': form})

@login_required
def feedback_update(request, feedback_id):
    # Get the feedback to be updated (ensure that the feedback belongs to the logged-in user)
    feedback = get_object_or_404(Feedback, pk=feedback_id, utilisateur=request.user)
    
    # If the form is submitted, process the update
    if request.method == "POST":
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback updated successfully.")
            return redirect('feedback_list')  # Redirect to the feedback list after successful update
    else:
        # If not POST, display the form with the current data
        form = FeedbackForm(instance=feedback)
    
    # Pass the form and feedback to the template context
    return render(request, 'Feedback/feed_update.html', {'form': form, 'feedback': feedback})


@login_required
def feedback_delete(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    
    # Check if the feedback belongs to the logged-in user
    if feedback.utilisateur != request.user:
        return redirect('feedback_list')  # Redirect back to the feedback list page if not authorized
    
    feedback.delete()
    messages.success(request, "Feedback deleted successfully.")
    return redirect('feedback_list')  # Corrected redirection to feedback list after deletion

