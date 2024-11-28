from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment_Pos
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
        form = self.form_class(request.POST, request.FILES)  # Use POST and FILES data

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
    


   
    

    




class Details(LoginRequiredMixin,DetailView):
    model=Post
    
    template_name="Blog/blog_detail.html"
    
    context_object_name="posts"



    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        
        poste = self.get_object()
        
        context['comments'] = Comment_Pos.objects.filter(post=poste)
        return context
    
def detailsPoste(request,ide):
    
    poste= Post.objects.get(id=ide)
    
    return render(request,"Blog/blog_detail.html",{"posts":poste})


    


class AddPoste(CreateView):
    model = Post
    template_name = "Blog/blog_form.html"
    form_class = PostForm
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        # Set the currently logged-in user as the `auteur`
        form.instance.auteur = self.request.user
        return super().form_valid(form)
    
    


class UpdatePoste(UpdateView):
    model=Post
    template_name="Blog/blog_form.html"
    form_class=PostForm
    success_url=reverse_lazy('list')
    
     
     
     
     
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
    

def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        # Unlike the post
        post.likes.remove(user)
    else:
        # Like the post
        post.likes.add(user)
        # Create a notification for the author
        if post.auteur != user:
            Notification.objects.create(
                user=post.auteur,
                message=f"{user.first_name} liked your post '{post.titre}'."
            )
    return redirect('list')






