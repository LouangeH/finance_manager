from django.db import models
from django.contrib.auth.models import User
from app.models import CategorieBank

class BankOperation(models.Model):
    TYPE_CHOICES = [
        ('depot', 'Dépôt'),
        ('retrait', 'Retrait'),
        ('tenue', 'Tenue de compte'),
    ]

    bank = models.ForeignKey(CategorieBank, on_delete=models.CASCADE, related_name="bank")
    type_operation = models.CharField(max_length=10, choices=TYPE_CHOICES)
    montant = models.DecimalField(max_digits=12, decimal_places=0)
    motif = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_operation_display()} de {self.montant} FBu le {self.date.date()}"

    class Meta:
        verbose_name = "Opération bancaire"
        verbose_name_plural = "Opérations bancaires"

class BankTransfert(models.Model):
    banque_source = models.ForeignKey(CategorieBank, related_name="transferts_sortants", on_delete=models.CASCADE)
    banque_destination = models.ForeignKey(CategorieBank, related_name="transferts_entrants", on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=12, decimal_places=0)
    motif = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfert de {self.montant} FBu de {self.banque_source} vers {self.banque_destination} le {self.date.date()}"

