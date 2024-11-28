

from django.db import models
from user.models import Utilisateur



class Feedback(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="feedbacks")
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('closed', 'Closed')], default='open')
    feedback_type = models.CharField(max_length=20, choices=[('general', 'General Feedback'), ('suggestion', 'Suggestion'), ('issue', 'Issue')], default='general')
    description_feedback = models.TextField()
    need_admin = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(
        null=True, 
        blank=True, 
        choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]
    )

    def __str__(self):
        return f"{self.feedback_type} - {self.status}"
