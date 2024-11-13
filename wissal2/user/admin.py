from django.contrib import admin
from .models import Utilisateur

# Register your models here.

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name', 'email')
    list_filter = (['email'])
    search_fields = ('email', 'first_name', 'last_name')
    ordering = (['first_name'])
