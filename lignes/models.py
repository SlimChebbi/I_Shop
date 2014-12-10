from django.db import models


class Ligne(models.Model):
    choice = (('Ooredoo', 'Ooredoo'), ('Orange', 'Orange'),
              ('Telecom', 'Telecom'))
    forfait = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=choice)
    prix_de_gros = models.DecimalField(max_digits=10, decimal_places=3)
    prix = models.DecimalField(max_digits=10, decimal_places=3)
    quantite = models.IntegerField()
    description = models.CharField(max_length=2500, blank=True, null=True)

    def __unicode__(self):
        return "Ligne" + self.name

    class Meta:
        db_table = 'Ligne'
