from django.shortcuts import render, redirect, get_object_or_404
from core.forms import CompteForm
from core.models import Compte
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def compte_list(request):
    comptes = Compte.objects.all().order_by('-date')
    paginator = Paginator(comptes, 10)  # 10 achats par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'comptes/compte_list.html', {'page_obj': page_obj, 'comptes': comptes})


def create_compte(request):
    form = CompteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('compte_list')
    return render(request, 'comptes/create_compte.html', {'form': form})


def edit_compte(request, pk):
    comptes = get_object_or_404(Compte, pk=pk)
    form = CompteForm(request.POST or None, instance=comptes)
    if form.is_valid():
        form.save()
        return redirect('compte_list')
    
    return render(request, 'comptes/create_compte.html', {'form': form, 'comptes': comptes})


def delete_compte(request, pk):
    comptes = get_object_or_404(Compte, pk=pk)
    if request.method == 'POST':
        comptes.delete()
        return redirect('compte_list')
    return render(request, 'comptes/delete_compte.html', {'comptes': comptes})


