from user.models import Utilisateur
from django.db import models

class Event(models.Model):
    nom_event = models.CharField(max_length=100)
    image_url = models.URLField()
    description_event = models.TextField()
    date_event = models.DateTimeField()
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nombre_places_disponibles = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    #u_event=models.ManyToManyField(Utilisateur, through="User_Event", related_name="eve")

    def __str__(self):
        return self.nom_event

class User_Event(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    nombre_places_achete = models.IntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('utilisateur', 'event')


