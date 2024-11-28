from django import forms
from .models import Post,Comment_Pos

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = '__all__'
        
        exclude=('auteur','likes')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment_Pos
        fields = ['texte']
