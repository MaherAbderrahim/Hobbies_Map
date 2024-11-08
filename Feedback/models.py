

from django.db import models
from Utilisateur.models import User

class Feedback(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=50)
    description_feedback = models.TextField()
    url_images_feedback = models.URLField()
    need_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback de {self.utilisateur} - {self.statut}"
