from django.db import models
from Utilisateur.models import User

class Sponsor(models.Model):
    nom_sponsor = models.CharField(max_length=100)
    description_sponsor = models.TextField()
    prix_sponsor = models.DecimalField(max_digits=10, decimal_places=2)
    url_site = models.URLField()
    url_photos = models.URLField()
    rentabilite_par_user = models.FloatField()
    sponsor = models.ManyToManyField(User, through="User_Sponsor", related_name="spons")
    def __str__(self):
        return self.nom_sponsor

class User_Sponsor(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_clics = models.IntegerField()
    nombre_apparitions = models.IntegerField()
