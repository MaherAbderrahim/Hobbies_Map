from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment_Pos,PostLike
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from .models import Notification
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json


# Create your views here.
from django.views.generic import *
from django.http.response import HttpResponse
# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy

import joblib  # for loading the model
from tensorflow.keras.models import load_model
# Load the trained model and vectorizer
model = load_model('toxic_comment_prediction_model.h5')
vectorizer = joblib.load('tfidf_vectorizer.pkl')
vectorizer2 = joblib.load('vectorizer2.pkl')
model2=joblib.load('toxic_poste_model.pkl')

@login_required
def list(request):
    postes = Post.objects.all().order_by('-date_creation')
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    return render(request, 'Blog/blog_list.html', {"posts": postes, "notifications": notifications})

    
    
    
    
from django.db.models import Q

from django.shortcuts import redirect
from django.views.generic import ListView
from .models import Post, Comment_Pos, Notification
from .forms import PostForm

class ListPoste(ListView):
    model = Post
    template_name = "Blog/blog_list.html"
    context_object_name = "posts"
    form_class = PostForm

    
        
     

    def post(self, request, *args, **kwargs):
        # Handle POST request: form submission to create a new post
        form = self.form_class(request.POST, request.FILES) 
        contenu = request.POST.get('contenu', None)
        print(contenu) # Use POST and FILES data
        text = contenu
        add_poste_view = AddPoste()
        add_poste_view.request = request 
        if text:
            # Preprocess the text (vectorization)
            text_vectorized = vectorizer.transform([text])
            text2=vectorizer2.transform([text])
            # Get the model's prediction
            prediction = model.predict(text_vectorized.toarray())
            prediction2=model2.predict(text2)
            print("Prediction:", prediction)
            print("Prediction2:", prediction2)
            # Determine if the text is toxic (1 for toxic, 0 for non-toxic)
            toxic = 1 if prediction2[0] and prediction[0] > 0.5 else 0
        else:
            toxic = 0
        
        # If the comment is toxic, do not allow form validation and return an error message
        if toxic == 1:
            form.add_error('contenu', f'This post is toxic with a score of {prediction[0]} and cannot be submitted.')
            self.object_list = self.get_queryset()
            queryset = self.get_queryset()
            context = self.get_context_data(form=form, queryset=queryset)
            context['alert_message'] = f"This post is toxic with a score of {prediction[0]} and cannot be submitted."
            form = self.form_class()  # Reset the form to be empty
            context['form'] = form
            return self.render_to_response(context)
        
        if form.is_valid():
            # Set the currently logged-in user as the `auteur`
            form.instance.auteur = request.user
            form.save()  # Save the new post

            # Redirect to the list page after successful form submission
            return redirect('list')  # Adjust to the name of your view's URL

        # If the form is invalid, re-render the page with errors
        queryset = self.get_queryset()
        context = self.get_context_data(form=form, queryset=queryset)
        context['error'] = "Form submission failed. Please check for errors."
        Notification.objects.filter(user=self.request.user, is_read=False).update(user=self.request.user,is_read=True)
        return self.render_to_response(context)

    def get_queryset(self):
        # Custom filtering logic based on GET parameters
        queryset = super().get_queryset()

        # Get filter parameters from the request
        category = self.request.GET.get("category")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        # Filter by category if provided
        if category:
            queryset = queryset.filter(category=category)

        # Filter by date range if provided
        if start_date and end_date:
            if start_date > end_date:
                return queryset.none()  # Return no results in case of error
            queryset = queryset.filter(date_creation__range=[start_date, end_date])

        return queryset

    def get_context_data(self, **kwargs):
        # Add form and other context data to the template
        context = super().get_context_data(**kwargs)
        
        # Fetch all comments and notifications for the user
        context['comments'] = Comment_Pos.objects.all()
        context['notifications'] = Notification.objects.filter(user=self.request.user, is_read=False)
        context['likes']=PostLike.objects.filter(user=self.request.user)
        
        
        # Add current filter parameters to the context for use in the template
        context['categories'] = Post.objects.values_list('category', flat=True).distinct()
        context['selected_category'] = self.request.GET.get("category", "")
        context['start_date'] = self.request.GET.get("start_date", "")
        context['end_date'] = self.request.GET.get("end_date", "")
        
        # Include the form in context to render it in the template
        context['form'] =self.form_class()

        # Handle date range error message
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if start_date and end_date and start_date > end_date:
            context['error'] = "Start date cannot be after end date."

        return context
    


   
    

    






class Details(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "Blog/blog_detail.html"
    context_object_name = "posts"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poste = self.get_object()  # Get the current post object
        context['form'] = self.form_class()  # Add the comment form to the context
        context['comments'] = Comment_Pos.objects.filter(post=poste)
        print(context['comments'])  # Fetch the comments for this post
        return context

    def post(self, request, *args, **kwargs):
        """ Handle POST request for comment submission. """
        form = self.form_class(request.POST)  # Get form data from request
        
        if form.is_valid():
            # Get the post object and associate it with the new comment
            post = self.get_object()  # Fetch the post
            form.instance.utilisateur = request.user  # Set the logged-in user as the comment author
            form.instance.post = post  # Link the comment to the post

            form.save()  # Save the comment

            # Redirect to the current post detail view after successful form submission
            return redirect('detailsClass', pk=post.pk)

        # If form is invalid, render the page again with the form errors and comments
        context = self.get_context_data(form=form)
        context['error'] = "Form submission failed. Please check for errors."
        return self.render_to_response(context)

    
    
def detailsPoste(request,ide):
    
    poste= Post.objects.get(id=ide)
    comments =Comment_Pos.objects.filter(post=poste)
    return render(request,"Blog/blog_detail.html",{"posts":poste,"comments":comments})


    


class AddPoste(CreateView):
    model = Post
    template_name = "Blog/blog_form.html"
    form_class = PostForm
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        # Set the currently logged-in user as the `auteur`
        form.instance.auteur = self.request.user
        text = form.instance.contenu
        if text:
            # Preprocess the text (vectorization)
            text_vectorized = vectorizer.transform([text])
            text2=vectorizer2.transform([text])
            # Get the model's prediction
            prediction = model.predict(text_vectorized.toarray())
            prediction2=model2.predict(text2)
            print("Prediction:", prediction)
            print("Prediction2:", prediction2)
            # Determine if the text is toxic (1 for toxic, 0 for non-toxic)
            toxic = 1 if prediction2[0] > 0.5 else 0
        else:
            toxic = 0
        
        # If the comment is toxic, do not allow form validation and return an error message
        if toxic == 1:
            form.add_error('contenu', f'This post is toxic with a score of {prediction2[0]} and cannot be submitted.')
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
    


class UpdatePoste(UpdateView):
    model=Post
    template_name="Blog/blog_form.html"
    form_class=PostForm
    success_url=reverse_lazy('list')
    def form_valid(self, form):
        # Set the currently logged-in user as the `auteur`
        form.instance.auteur = self.request.user
        text = form.instance.contenu
        if text:
            # Preprocess the text (vectorization)
            text_vectorized = vectorizer.transform([text])
            text2=vectorizer2.transform([text])
            # Get the model's prediction
            prediction = model.predict(text_vectorized.toarray())
            prediction2=model2.predict(text2)
            print("Prediction:", prediction)
            print("Prediction2:", prediction2)
            # Determine if the text is toxic (1 for toxic, 0 for non-toxic)
            toxic = 1 if prediction2[0] > 0.5 else 0
        else:
            toxic = 0
        
        # If the comment is toxic, do not allow form validation and return an error message
        if toxic == 1:
            form.add_error('contenu', f'This post is toxic with a score of {prediction2[0]} and cannot be submitted.')
            return self.form_invalid(form)
        
        return super().form_valid(form)
     
     
     
     
class DeletePoste(DeleteView):
    
    model=Post
    template_name="Blog/blog_delete.html"
    success_url=reverse_lazy('list')
# CRUD pour Post

def home(request):
    return render(request, 'Blog/index.html')


def notifications(request):
    Notification.objects.filter(user=request.user, is_read=False).update(user=request.user,is_read=True)
    return redirect('list')
    

from django.shortcuts import get_object_or_404, redirect
from Blog.models import Post, PostLike

def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    reaction = request.POST.get('reaction')  # Get the reaction from the form

    # Define reaction-based messages
    reaction_messages = {
        'like': "liked your post",
        'love': "loved your post",
        'haha': "laughed at your post",
        'angry': "got angry at your post",
        'sad': "was sad about your post"
    }

    # Ensure the reaction is valid
    if reaction not in reaction_messages:
        reaction = 'like'  # Default to "like" if an invalid reaction is received

    # Check if the user has already reacted to the post
    existing_reaction = PostLike.objects.filter(user=user, post=post).first()

    if existing_reaction:
        # If the reaction already exists, remove it (unlike/unreact)
        existing_reaction.delete()
    else:
        # Add a new reaction
        PostLike.objects.create(user=user, post=post,reaction=reaction)

        # Create a notification for the author based on the selected reaction
        if post.auteur != user:
            notification_message = f"{user.first_name} {reaction_messages.get(reaction)} '{post.titre}'."
            Notification.objects.create(
                user=post.auteur,
                message=notification_message
            )

    return redirect('list')







class CommentListView(ListView):
    model = Comment_Pos
    template_name = "Blog/blog_detail.html"
    context_object_name = 'comments'
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment_Pos.objects.filter(post__id=post_id)
    

class AddCommentView(CreateView):
    model = Comment_Pos
    form_class = CommentForm
    template_name = 'Blog/blog_detail.html'
    
    def form_valid(self, form):
        form.instance.utilisateur = self.request.user  # Automatically set the logged-in user as the author
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])  # Link comment to the post
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})