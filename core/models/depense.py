from django.db import models
from core.models.compte import Compte
from core.models.depense_cat import CategorieDepense
from django.utils import timezone

class Depense(models.Model):
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    categorie = models.ForeignKey(CategorieDepense, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.description} - {self.montant}"