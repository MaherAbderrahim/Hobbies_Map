# forms.py
from django import forms
from .models import Post, Comment_Pos

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titre', 'contenu']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment_Pos
        fields = ['texte']
