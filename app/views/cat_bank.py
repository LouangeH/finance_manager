from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.models import CategorieBank
from app.forms import CategorieBankForm
from django.core.paginator import Paginator
from django.db.models import Sum, Q

@login_required
def bank_list(request):
    banks = CategorieBank.objects.order_by('-id')  # ou '-date' si tu as un champ date
    bank_data = []

    for bank in banks:
        operations = bank.bank.all()  # related_name="bank" depuis ForeignKey

        total_depot = operations.filter(type_operation='depot').aggregate(total=Sum('montant'))['total'] or 0
        total_retrait = operations.filter(type_operation='retrait').aggregate(total=Sum('montant'))['total'] or 0
        total_tenue = operations.filter(type_operation='tenue').aggregate(total=Sum('montant'))['total'] or 0

        solde = total_depot - (total_retrait + total_tenue)

        bank_data.append({
            'bank': bank,
            'solde': solde
        })

    # Pagination manuelle (sur bank_data)
    paginator = Paginator(bank_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bank/bank_list.html', {'page_obj': page_obj})


@login_required
def create_bank(request):
    form = CategorieBankForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('bank_list')
    return render(request, 'bank/create_bank.html', {'form': form})


@login_required
def update_bank(request, pk):
    banks = get_object_or_404(CategorieBank, pk=pk)
    form = CategorieBankForm(request.POST or None, instance=banks)
    if form.is_valid():
        form.save()
        return redirect('bank_list')
    return render(request, 'bank/create_bank.html', {'form': form})


@login_required
def delete_bank(request, pk):
    banks = get_object_or_404(CategorieBank, pk=pk)
    if request.method == 'POST':
        banks.delete()
        return redirect('bank_list')
    return render(request, 'bank/confirm_delete1.html', {'banks': banks})
