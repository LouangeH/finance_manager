from django.db.models import Sum
from django.shortcuts import render
from app.models import Depense, Revenu, BankOperation, BudgetMensuel
from django.contrib.auth.decorators import login_required
from datetime import date

#@login_required
def dashboard(request):
    

    today = date.today()
    mois_actuel = today.replace(day=1)

    # Budgets
    budgets = BudgetMensuel.objects.filter(
        mois__year=mois_actuel.year,
        mois__month=mois_actuel.month
    )

    data = []
    for budget in budgets:
        depense_reelle = Depense.objects.filter(
            depense=budget.categorie,
            date__year=mois_actuel.year,
            date__month=mois_actuel.month
        ).aggregate(total=Sum('somme'))['total'] or 0

        ecart = depense_reelle - budget.montant_planifie
        data.append({
            'categorie': budget.categorie,
            'prevu': budget.montant_planifie,
            'reel': depense_reelle,
            'ecart': ecart,
            'alert': ecart > 0
        })

    depenses = Depense.objects.aggregate(Sum('somme'))['somme__sum'] or 0
    revenus = Revenu.objects.aggregate(Sum('somme'))['somme__sum'] or 0
    depots = BankOperation.objects.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
    retraits = BankOperation.objects.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
    solde_caisse = (revenus + retraits) - (depenses + depots)
    total_tenue = BankOperation.objects.filter(type_operation='tenue').aggregate(Sum('montant'))['montant__sum'] or 0
    solde_banque = depots - retraits - total_tenue

    return render(request, 'fuel/accueil.html', {
        'depenses': depenses,
        'revenus': revenus,
        'total_depots': depots,
        'total_retraits': retraits,
        'total_tenue': total_tenue,
        'solde_banque': solde_banque,
        'solde_caisse': solde_caisse,
        'budget_data': data,
        'mois': mois_actuel,
    })
