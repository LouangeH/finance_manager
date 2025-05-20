# models.py
from django.db import models
from app.models import CategorieDepense
from django.utils import timezone

class BudgetMensuel(models.Model):
    TYPE_CHOICES = [
        ('depense', 'Dépense'),
        ('epargne', 'Épargne'),
        ('achat', 'Achat'),
        ('autre', 'Autre')
    ]

    mois = models.DateField(help_text="Choisir le mois du budget (ex: 2025-06-01)")
    categorie = models.ForeignKey(CategorieDepense, on_delete=models.CASCADE)
    montant_planifie = models.DecimalField(max_digits=12, decimal_places=0)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    objectif = models.CharField(max_length=255, blank=True)
    prioritaire = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mois', 'categorie')
        verbose_name = "Budget mensuel"
        verbose_name_plural = "Budgets mensuels"

    def __str__(self):
        return f"{self.mois.strftime('%B %Y')} - {self.categorie} : {self.montant_planifie} FBu"
