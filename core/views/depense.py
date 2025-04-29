from django.shortcuts import render, redirect, get_object_or_404
from core.forms import DepenseForm
from core.models import Depense
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def depense_list(request):
    depenses = Depense.objects.all().order_by('-date')
    paginator = Paginator(depenses, 10)  # 10 achats par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'depenses/depense_list.html', {'page_obj': page_obj, 'depenses': depenses})


def create_depense(request):
    form = DepenseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('depense_list')
    return render(request, 'depenses/create_depense.html', {'form': form})


def edit_depense(request, pk):
    depenses = get_object_or_404(Depense, pk=pk)
    form = DepenseForm(request.POST or None, instance=depenses)
    if form.is_valid():
        form.save()
        return redirect('depense_list')
    
    return render(request, 'depenses/create_depense.html', {'form': form, 'depenses': depenses})


def delete_depense(request, pk):
    depenses = get_object_or_404(Depense, pk=pk)
    if request.method == 'POST':
        depenses.delete()
        return redirect('depense_list')
    return render(request, 'depenses/delete_depense.html', {'depenses': depenses})


