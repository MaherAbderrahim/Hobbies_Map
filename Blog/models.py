from user.models import Utilisateur
from django.db import models
from django.core.validators import  FileExtensionValidator

class Post(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    photo = models.FileField(upload_to='photos/')
    likes = models.ManyToManyField(Utilisateur, related_name='liked_posts', blank=True)
    CATEGORY_CHOICES = [
        ('Tech', 'Technology'),
        ('Health', 'Health'),
        ('Lifestyle', 'Lifestyle'),
        ('Education', 'Education'),
        ('Environment', 'Environment'),
        ('Sports', 'Sports'),
        ('Jeux', 'Jeux'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    def __str__(self):
        return self.titre

class Comment_Pos(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    texte = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.texte

class Notification(models.Model):
    user = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='notifications'
    )  # The user who receives the notification
    message = models.TextField()  # The notification content
    is_read = models.BooleanField(default=False)  # Whether the notification has been read
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the notification was created

    def __str__(self):
        return f"Notification for {self.user.email} - {self.message[:50]}"

    def mark_as_read(self):
        """
        Marks the notification as read and saves the change.
        """
        self.is_read = True
        self.save()