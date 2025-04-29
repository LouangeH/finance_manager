from django.db import models
from core.models.compte import Compte
from django.utils import timezone

class TransfertFonds(models.Model):
    source = models.ForeignKey(Compte, related_name='transferts_sortants', on_delete=models.CASCADE)
    destination = models.ForeignKey(Compte, related_name='transferts_entrants', on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.montant} de {self.source} à {self.destination}"