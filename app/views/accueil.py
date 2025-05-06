from django.db.models import Sum
from django.shortcuts import render
from app.models import Depense, Revenu, BankOperation
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    depenses = Depense.objects.aggregate(Sum('somme'))['somme__sum'] or 0
    revenus = Revenu.objects.aggregate(Sum('somme'))['somme__sum'] or 0

    depots = BankOperation.objects.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
    retraits = BankOperation.objects.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
    solde_caisse = (revenus + retraits) - (depenses + depots)
    total_depots = BankOperation.objects.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
    total_retraits = BankOperation.objects.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
    total_tenue = BankOperation.objects.filter(type_operation='tenue').aggregate(Sum('montant'))['montant__sum'] or 0

    solde_banque = total_depots - total_retraits - total_tenue
    

    context = {
        'depenses': depenses,
        'revenus': revenus,
        'total_depots': total_depots,
        'total_retraits': total_retraits,
        'total_tenue': total_tenue,
        'solde_banque': solde_banque,
        'solde_caisse': solde_caisse,
    }
    return render(request, 'fuel/accueil.html', context)