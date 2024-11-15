

from django.db import models
from user.models import Utilisateur

class Feedback(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed')
    ]

    statut = models.CharField(max_length=20, choices=STATUS_CHOICES)
    description_feedback = models.TextField()
    need_admin = models.BooleanField(default=False)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"Feedback by {self.utilisateur} "