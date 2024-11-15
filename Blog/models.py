from user.models import Utilisateur
from django.db import models
from django.core.validators import  FileExtensionValidator

class Post(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    photo = models.FileField(upload_to='photos/')
    
    def __str__(self):
        return self.titre

class Comment_Pos(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    texte = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texte

