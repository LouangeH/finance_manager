from django.db import models
from django.db.models import Sum

class CategorieBank(models.Model):
    categorie = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.categorie}"
    
    def get_solde(self):
        operations = self.bank.all()  # dépend de related_name dans ForeignKey
        total_depots = operations.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
        total_retraits = operations.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
        total_tenue = operations.filter(type_operation='tenue').aggregate(Sum('montant'))['montant__sum'] or 0
        return total_depots - total_retraits - total_tenue