from django.http import JsonResponse
from django.db.models import Sum
from app.models import BankOperation, CategorieBank

def get_bank_solde(request, bank_id):
    try:
        bank = CategorieBank.objects.get(pk=bank_id)
        operations = bank.bank.all()
        total_depot = operations.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
        total_retrait = operations.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
        total_tenue = operations.filter(type_operation='tenue').aggregate(Sum('montant'))['montant__sum'] or 0
        solde = total_depot - total_retrait - total_tenue
        return JsonResponse({'solde': solde})
    except CategorieBank.DoesNotExist:
        return JsonResponse({'solde': 0})
