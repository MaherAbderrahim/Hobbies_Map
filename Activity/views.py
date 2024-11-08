from django.views.generic import ListView, CreateView, UpdateView,DeleteView,DetailView
from .models import Activity, Category
from .forms import ActivityForm, CategoryForm

# Vue pour afficher la liste des activités
class ActivityListView(ListView):
    model = Activity
    template_name = 'Activity/act_list.html'
    context_object_name = 'activities'

# Vue pour ajouter une nouvelle activité
class ActivityCreateView(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'Activity/act_form.html'
    success_url = '/activities/'

# Vue pour modifier une activité existante
class ActivityUpdateView(UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'Activity/act_form.html'
    success_url = '/activities/'

# Vue pour supprimer une activité existante
class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = 'Activity/act_delete.html'
    success_url = '/activities/'

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
    success_url = '/activities/categories/'

# Vue pour modifier une catégorie existante
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'Category/form.html'
    success_url = '/activities/categories/'

# Vue pour supprimer une catégorie existante
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'Category/delete.html'
    success_url = '/activities/categories/'

# Vue pour afficher le détail d'une activité
class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'Activity/act_detail.html'
    context_object_name = 'activity'

