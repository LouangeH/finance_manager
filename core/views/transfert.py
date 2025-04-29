from django.shortcuts import render, redirect, get_object_or_404
from core.forms import TransfertFondsForm
from core.models import TransfertFonds
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def transfert_list(request):
    transferts = TransfertFonds.objects.all().order_by('-date')
    paginator = Paginator(transferts, 10)  # 10 achats par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'transferts/transfert_list.html', {'page_obj': page_obj, 'transferts': transferts})


def create_transfert(request):
    form = TransfertFondsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('transfert_list')
    return render(request, 'transferts/create_transfert.html', {'form': form})


def edit_transfert(request, pk):
    transferts = get_object_or_404(TransfertFonds, pk=pk)
    form = TransfertFondsForm(request.POST or None, instance=transferts)
    if form.is_valid():
        form.save()
        return redirect('transfert_list')
    
    return render(request, 'transferts/create_transfert.html', {'form': form, 'transferts': transferts})


def delete_transfert(request, pk):
    transferts = get_object_or_404(TransfertFonds, pk=pk)
    if request.method == 'POST':
        transferts.delete()
        return redirect('transfert_list')
    return render(request, 'transferts/delete_transfert.html', {'transferts': transferts})


