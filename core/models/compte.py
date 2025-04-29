from django.db import models
from django import forms
from django.utils import timezone

class Compte(models.Model):
    TYPE_CHOICES = [
        ('portefeuille', 'Portefeuille'),
        ('coffre', 'Coffre (Argent de secours)'),
        ('courant', 'Compte courant'),
        ('epargne', 'Compte épargne'),
    ]

    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    solde_initial = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    date_ouverture = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"