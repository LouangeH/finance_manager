from django.db import models
from app.models import CategorieRevenue

class Revenu(models.Model):
    revenu = models.ForeignKey(CategorieRevenue, on_delete=models.CASCADE, related_name="revenu")
    source = models.CharField(max_length=100)
    somme = models.DecimalField(max_digits=10, decimal_places=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.somme} FBu provenu a {self.source} le {self.date.date()}"
