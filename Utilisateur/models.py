from django.db import models
from django.contrib.auth.models import AbstractUser  # Importation du modèle d'utilisateur abstrait de Django.


class User(AbstractUser):
    nom_user = models.CharField(max_length=100)
    prenom_user = models.CharField(max_length=100)
    email_user = models.EmailField(unique=True)
    is_premium_user = models.BooleanField(default=False)
    abonnement_user = models.BooleanField(default=False)
    def __str__(self):
        return self.prenom_user
    class Meta:
        verbose_name = "User"
    

