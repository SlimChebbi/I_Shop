from django.db import models
from accessoires.models import *
from portables.models import *
from lignes.models import *

# Create your models here.


class Vendre(models.Model):
    acces = models.ForeignKey(Accessoire, blank=True, null=True)
    port = models.ForeignKey(Portable, blank=True, null=True)
    ligne = models.ForeignKey(Ligne, blank=True, null=True)

    item = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    prix_de_gros = models.DecimalField(max_digits=10, decimal_places=3)
    prix_de_vendre = models.DecimalField(max_digits=10, decimal_places=3)
    quantite = models.IntegerField()
    note = models.CharField(max_length=2500, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.CharField(max_length=255)
    reparation = models.IntegerField(blank=True, null=True)
    image = models.FileField(upload_to='acessoire/', blank=True, null=True)

    def __unicode__(self):
        return "Vendre" + self.produit

    class Meta:
        db_table = 'Vendre'
