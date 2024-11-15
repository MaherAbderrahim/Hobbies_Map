from django.db import models

class Sponsor(models.Model):
    nom_sponsor = models.CharField(max_length=100)
    description_sponsor = models.TextField()
    prix_sponsor = models.DecimalField(max_digits=10, decimal_places=2)
    url_site = models.URLField()
    url_photos = models.URLField()
    rentabilite_par_user = models.FloatField()
    def __str__(self):
        return self.nom_sponsor

