from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment_Pos
from .forms import PostForm, CommentForm

from django.shortcuts import render



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
    
    return render(request ,'Blog/blog_list.html' , {"posts" :postes})
    
    
    
    
    
class ListPoste(ListView):
    model=Post
    template_name="Blog/blog_list.html"
    context_object_name="posts"
    
    
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        
        context['comments']= Comment_Pos.objects.all()
        
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
