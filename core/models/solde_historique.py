from django.db import models
from core.models.compte import Compte

class HistoriqueSolde(models.Model):
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)
    mois = models.DateField()  # On stocke la date du 1er jour du mois
    solde = models.DecimalField(max_digits=12, decimal_places=0)

    class Meta:
        unique_together = ('compte', 'mois')