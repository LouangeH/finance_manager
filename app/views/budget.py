# views.py
from django.shortcuts import render, redirect, get_object_or_404
from app.models import BudgetMensuel, Depense, Revenu, BankOperation
from app.forms import BudgetMensuelForm
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date
from django.db.models import Sum


def budget_list(request):
    budgets = BudgetMensuel.objects.all().order_by('-mois')
    paginator = Paginator(budgets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'budget/budget_list.html', {'budgets': page_obj, 'page_obj': page_obj})


def create_budget(request):
    form = BudgetMensuelForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Budget enregistré avec succès.")
        return redirect('budget_list')
    else:
        print(form.errors)  # pour debug dans la console serveur
    return render(request, 'budget/budget_form.html', {'form': form})


def update_budget(request, pk):
    budget = get_object_or_404(BudgetMensuel, pk=pk)
    form = BudgetMensuelForm(request.POST or None, instance=budget)
    if form.is_valid():
        form.save()
        messages.success(request, "Budget mis à jour avec succès.")
        return redirect('budget_list')
    return render(request, 'budget/budget_form.html', {'form': form})


def delete_budget(request, pk):
    budget = get_object_or_404(BudgetMensuel, pk=pk)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, "Budget supprimé.")
        return redirect('budget_list')
    return render(request, 'budget/budget_confirm_delete.html', {'budget': budget})


def dashboard_budget_mensuel(request):
    today = date.today()
    mois_actuel = today.replace(day=1)

    print(">>> VUE Budget Mensuel appelée")
    mois_actuel = date.today().replace(day=1)
    print(">>> Mois actuel :", mois_actuel)
    
    # ⚠ Correction ici
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

    # Reste inchangé
    depenses = Depense.objects.aggregate(Sum('somme'))['somme__sum'] or 0
    revenus = Revenu.objects.aggregate(Sum('somme'))['somme__sum'] or 0
    depots = BankOperation.objects.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
    retraits = BankOperation.objects.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
    solde_caisse = (revenus + retraits) - (depenses + depots)
    total_depots = depots
    total_retraits = retraits
    total_tenue = BankOperation.objects.filter(type_operation='tenue').aggregate(Sum('montant'))['montant__sum'] or 0
    solde_banque = total_depots - total_retraits - total_tenue

    

    return render(request, 'fuel/accueil.html', {
        'depenses': depenses,
        'revenus': revenus,
        'total_depots': total_depots,
        'total_retraits': total_retraits,
        'total_tenue': total_tenue,
        'solde_banque': solde_banque,
        'solde_caisse': solde_caisse,
        'budget_data': data,
        'mois': mois_actuel
    })
