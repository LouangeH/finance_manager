from django.db import models
from core.models.compte import Compte
from django.utils import timezone

class Revenue(models.Model):
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    recurrent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.source} ({self.montant})"