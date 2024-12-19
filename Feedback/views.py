from django.shortcuts import render, redirect, get_object_or_404
from .models import Feedback
from .forms import FeedbackForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import joblib

vectorizer2 = joblib.load('vectorizer2.pkl')
model2=joblib.load('toxic_poste_model.pkl')


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
        contenu = request.POST.get('description_feedback', None)
        
        # Debugging logs
        print("Submitted feedback:", contenu)
        
        toxic = 0  # Default to non-toxic
        if contenu:
            try:
                # Preprocess the text (vectorization)
                text2 = vectorizer2.transform([contenu])
                
                # Get the model's prediction
                prediction2 = model2.predict(text2)
                print("Prediction score:", prediction2[0])
                
                # Determine toxicity based on the model's prediction
                toxic = 1 if prediction2[0] > 0.5 else 0
            except Exception as e:
                print("Error in toxicity prediction:", str(e))
                form.add_error(None, "An error occurred while analyzing the feedback. Please try again later.")
        
        if toxic == 1:
            # Add error to the form for toxic feedback
            form.add_error('description_feedback', f'This feedback is toxic  and cannot be submitted.')
            context = {
                'form': form,
                'rating_range': range(1, 6),
                'alert_message': f"This feedback is toxic and cannot be submitted.Please be polite",
            }
            return render(request, 'Feedback/feed_form.html', context)
        
        # Check if the form is valid
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.utilisateur = request.user  # Assign the logged-in user
            feedback.save()
            messages.success(request, "Feedback submitted successfully.")
            return redirect('feedback:feedback')
        else:
            # Form validation errors
            print("Form errors:", form.errors)
    else:
        form = FeedbackForm()

    # Render the form with additional context
    context = {
        'form': form,
        'rating_range': range(1, 6),
    }
    return render(request, 'Feedback/feed_form.html', context)



@login_required
def feedback_update(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id, utilisateur=request.user)
    alert_message = None  # Initialize alert_message to None

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        contenu = request.POST.get('description_feedback', None)

        toxic = 0  # Default to non-toxic
        if contenu:
            try:
                # Preprocess the text (vectorization)
                text2 = vectorizer2.transform([contenu])
                prediction2 = model2.predict(text2)
                toxic = 1 if prediction2[0] > 0.5 else 0
            except Exception as e:
                print("Error in toxicity prediction:", str(e))
                form.add_error(None, "An error occurred while analyzing the feedback. Please try again later.")

        if toxic == 1:
            # Add an error for toxic feedback
            alert_message = "This feedback is toxic and cannot be updated. Please be polite."
            form.add_error('description_feedback', alert_message)
        else:
            # Clear all errors if the feedback is not toxic
            form.errors.clear()
            if form.is_valid():
                # Save the valid feedback
                updated_feedback = form.save(commit=False)
                updated_feedback.utilisateur = request.user
                updated_feedback.save()
                messages.success(request, "Feedback updated successfully.")
                return redirect('feedback:feedback')

    else:
        form = FeedbackForm(instance=feedback)

    # Render the form with additional context
    context = {
        'form': form,
        'feedback': feedback,
        'rating_range': range(1, 6),
        'alert_message': alert_message,
    }
    return render(request, 'Feedback/feed_update.html', context)







@login_required
def feedback_delete(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id, utilisateur=request.user)
    feedback.delete()
    messages.success(request, "Feedback deleted successfully.")
    return redirect('feedback:feedback')  # Update this if needed to match your actual URL name

