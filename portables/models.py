from django.db import models


class Portable(models.Model):
    choice = (('Nouveau', 'Nouveau'), ('Occasion', 'Occasion'))
    marque = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=choice)
    prix_de_gros = models.DecimalField(max_digits=10, decimal_places=3)
    prix = models.DecimalField(max_digits=10, decimal_places=3)
    quantite = models.IntegerField()
    description = models.CharField(max_length=2500, blank=True, null=True)
    image = models.FileField(upload_to='portable/', blank=True, null=True)

    def __unicode__(self):
        return "Portable" + self.model

    class Meta:
        db_table = 'Portable'
