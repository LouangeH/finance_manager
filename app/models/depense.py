from django.db import models
from app.models import CategorieDepense

class Depense(models.Model):
    depense = models.ForeignKey(CategorieDepense, on_delete=models.CASCADE, related_name="revenu")
    description = models.CharField(max_length=100)
    somme = models.DecimalField(max_digits=10, decimal_places=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.somme} FBu a ete utilisé pour {self.description} le {self.date.date()}"
