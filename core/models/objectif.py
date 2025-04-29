from django.db import models

class Objectif(models.Model):
    PRIORITE_CHOICES = [
        ('basse', 'Basse'),
        ('moyenne', 'Moyenne'),
        ('haute', 'Haute'),
    ]

    nom = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    deadline = models.DateField()
    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='moyenne')
    realise = models.BooleanField(default=False)

    def __str__(self):
        return self.nom