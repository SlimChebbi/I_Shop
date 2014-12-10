from django.db import models


class Reparation(models.Model):

    item = models.CharField(max_length=255)
    client = models.CharField(max_length=255, blank=True, null=True)
    telephone_client = models.IntegerField()
    date_debut = models.DateTimeField(auto_now_add=True, blank=True)
    date_finish = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=2500, blank=True, null=True)
    status = models.CharField(max_length=1, default="E")
    add_user = models.CharField(max_length=255)
    finish_user = models.CharField(max_length=255)

    def __unicode__(self):
        return "Reparation" + self.id

    class Meta:
        db_table = 'Reparation'


class Piece(models.Model):
    reparation = models.ForeignKey('Reparation')
    item = models.CharField(max_length=255)
    prix_de_gros = models.DecimalField(max_digits=10, decimal_places=3)
    prix = models.DecimalField(max_digits=10, decimal_places=3)
    quantite = models.IntegerField()
    description = models.CharField(max_length=2500, blank=True, null=True)


class MainOuevre(models.Model):
    reparation = models.ForeignKey('Reparation')
    prix = models.DecimalField(max_digits=10, decimal_places=3)
    description = models.CharField(max_length=2500, blank=True, null=True)
