from django.shortcuts import render, redirect, get_object_or_404
from .models import Feedback
from .forms import FeedbackForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def feedback_list(request):
    # Get all feedbacks for the logged-in user
    feedbacks = Feedback.objects.filter(utilisateur=request.user).order_by('-created_at')

    # Search and filter
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    if search_query:
        feedbacks = feedbacks.filter(
            Q(description_feedback__icontains=search_query) |
            Q(feedback_type__icontains=search_query)
        )

    if status_filter:
        feedbacks = feedbacks.filter(status=status_filter)

    paginator = Paginator(feedbacks, 5)  # Show 5 feedbacks per page
    page_number = request.GET.get('page')
    page_feedbacks = paginator.get_page(page_number)

    context = {
        'feedbacks': page_feedbacks,
        'search_query': search_query,
        'status_filter': status_filter,
        'statuses': Feedback._meta.get_field('status').choices,  # Dynamically get status choices
        'star_range': range(1, 6),  # Add the range for stars
    }
    return render(request, 'user/feedback.html', context)


@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.utilisateur = request.user  # Directly assign `request.user` as it is a `Utilisateur`
            feedback.save()
            messages.success(request, "Feedback submitted successfully.")
            return redirect('feedback:feedback')
    else:
        form = FeedbackForm()
        # Pass the range to the context
    context = {
        'form': form,
        'rating_range': range(1, 6),
    }
    return render(request, 'Feedback/feed_form.html', context)


@login_required
def feedback_update(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id, utilisateur=request.user)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()  # Save the updated feedback
            messages.success(request, "Feedback updated successfully.")
            return redirect('feedback:feedback')  # Redirect to feedback list page (change 'feedback_list' to 'feedback')
    else:
        form = FeedbackForm(instance=feedback)
    context = {
        'form': form,
        'feedback': feedback,
        'rating_range': range(1, 6),
    }
    
    return render(request, 'Feedback/feed_update.html', context)





@login_required
def feedback_delete(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id, utilisateur=request.user)
    feedback.delete()
    messages.success(request, "Feedback deleted successfully.")
    return redirect('feedback:feedback')  # Update this if needed to match your actual URL name

