from django.shortcuts import render, get_object_or_404, redirect
from .models import Feedback
from .forms import FeedbackForm

# CRUD pour Feedback
def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks})

def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback_list')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form})

def feedback_update(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('feedback_list')
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'feedback/feedback_form.html', {'form': form})

def feedback_detail(request, id):
    feedback = get_object_or_404(Feedback, id=id)  # Récupère l'article avec l'ID spécifié
    return render(request, 'feedback/feedback_detail.html', {'feedback': feedback})

def feedback_delete(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.delete()
    return redirect('feedback_list')
