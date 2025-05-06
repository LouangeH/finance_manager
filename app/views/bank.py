from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.models import BankOperation, CategorieBank
from app.forms import BankOperationForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Sum
from django.utils.timezone import datetime

#@login_required
def bank_operation_list(request):
    operations = BankOperation.objects.all().order_by('-date')

    type_id = request.GET.get('type')
    if type_id:
        operations = operations.filter(bank_id=type_id)

    periode = request.GET.get('periode')
    if periode:
        try:
            annee, mois = map(int, periode.split('-'))
            operations = operations.filter(date__year=annee, date__month=mois)
        except ValueError:
            pass

    # Filtrage par type d'opération
    operation_type = request.GET.get('operation')
    if operation_type in ['depot', 'retrait', 'tenue']:
        operations = operations.filter(type_operation=operation_type)

    # Calcul du total filtré : dépôt - retrait - tenue
    depot_total = operations.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
    retrait_total = operations.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
    tenue_total = operations.filter(type_operation='tenue').aggregate(Sum('montant'))['montant__sum'] or 0
    total_filtre = depot_total - retrait_total - tenue_total


    # pagination (optionnel)
    from django.core.paginator import Paginator
    paginator = Paginator(operations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'operations': page_obj,
        'page_obj': page_obj,
        'categories': CategorieBank.objects.all(),
        'total_filtre': total_filtre,
        'current_year': datetime.today().year,
        'current_month': str(datetime.today().month).zfill(2),
    }
    return render(request, 'bank/operation_list.html', context)

#@login_required
def create_bank_operation(request):
    form = BankOperationForm(request.POST or None)
    if form.is_valid():
        operation = form.save(commit=False)
        operation.effectué_par = request.user
        operation.save()
        return redirect('bankoperation_list')
    return render(request, 'bank/create_operation.html', {'form': form})

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


#@login_required
def update_bank_operation(request, pk):
    operation = get_object_or_404(BankOperation, pk=pk)
    if operation.type_operation == 'tenue':
        return redirect('bankoperation_list')  # Interdit
    form = BankOperationForm(request.POST or None, instance=operation)
    if form.is_valid():
        form.save()
        return redirect('bankoperation_list')
    return render(request, 'bank/create_operation.html', {'form': form})


#@login_required
def delete_bank_operation(request, pk):
    operation = get_object_or_404(BankOperation, pk=pk)
    if operation.type_operation == 'tenue':
        return redirect('bankoperation_list')  # Interdit
    if request.method == "POST":
        operation.delete()
        return redirect('bankoperation_list')
    return render(request, 'bank/confirm_delete.html', {'operation': operation})
