from django.db import models
from Utilisateur.models import Utilisateur
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    nom_categ = models.CharField(max_length=100)
    desc_categ = models.TextField()
    is_specifique = models.BooleanField(default=False)

    def __str__(self):
        return self.nom_categ

class Activity(models.Model):
    nom_activite = models.CharField(max_length=100)
    description_activite = models.TextField()
    prix_activite = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    localisation = models.CharField(max_length=255)
    note_moyenne = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    icone_map = models.CharField(max_length=255)
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="activites")
    #reservation = models.ManyToManyField(Utilisateur, through="User_Activity", related_name="act")

    def __str__(self):
        return self.nom_activite

class User_Activity(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    note = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        unique_together = ('utilisateur', 'activity')
    
    def __str__(self):
        return self.utilisateur.username + " " + self.activity.nom_activite

class Image_Activity(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="images")
    url_img = models.URLField()
    ordre_img = models.IntegerField()

    def __str__(self):
        return self.url_img

class Comment_Act(models.Model):
    text_comm = models.TextField()
    is_ban = models.BooleanField(default=False)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return f"Commentaire de {self.utilisateur} sur {self.activity}"
