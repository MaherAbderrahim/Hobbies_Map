from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Activity, Category
from .forms import ActivityForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Vue pour afficher la liste des activités
@method_decorator(login_required, name='dispatch')
class ActivityListView(ListView):
    model = Activity
    template_name = 'Activity/act_list.html'
    context_object_name = 'activities'

# Vue pour ajouter une nouvelle activité
@method_decorator(login_required, name='dispatch')
class ActivityCreateView(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'Activity/act_form.html'
    success_url = reverse_lazy('act_list')

# Vue pour modifier une activité existante
@method_decorator(login_required, name='dispatch')
class ActivityUpdateView(UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'Activity/act_form.html'
    success_url = reverse_lazy('act_list')

# Vue pour supprimer une activité existante
@method_decorator(login_required, name='dispatch')
class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = 'Activity/act_delete.html'
    success_url = reverse_lazy('act_list')

# Vue pour afficher le détail d'une activité
@method_decorator(login_required, name='dispatch')
class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'Activity/act_detail.html'
    context_object_name = 'activity'
# Vue pour afficher la liste des catégories
class CategoryListView(ListView):
    model = Category
    template_name = 'Category/list.html'
    context_object_name = 'categories'

# Vue pour ajouter une nouvelle catégorie
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'Category/form.html'
    success_url = reverse_lazy('category_list')  # Use named URL reversal

# Vue pour modifier une catégorie existante
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'Category/form.html'
    success_url = reverse_lazy('category_list')  # Use named URL reversal

# Vue pour supprimer une catégorie existante
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'Category/delete.html'
    success_url = reverse_lazy('category_list')  # Use named URL reversal
