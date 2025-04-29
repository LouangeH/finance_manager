from django.shortcuts import render, redirect, get_object_or_404
from core.forms import CategorieDepenseForm
from core.models import CategorieDepense
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def depense_cat_list(request):
    depense_cats = CategorieDepense.objects.all().order_by('-date')
    paginator = Paginator(depense_cats, 10)  # 10 achats par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'depense_cats/depense_cat_list.html', {'page_obj': page_obj, 'depense_cats': depense_cats})


def create_depense_cat(request):
    form = CategorieDepenseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('depense_cat_list')
    return render(request, 'depense_cats/create_depense_cat.html', {'form': form})


def edit_depense_cat(request, pk):
    depense_cats = get_object_or_404(CategorieDepense, pk=pk)
    form = CategorieDepenseForm(request.POST or None, instance=depense_cats)
    if form.is_valid():
        form.save()
        return redirect('depense_cat_list')
    
    return render(request, 'depense_cats/create_depense_cat.html', {'form': form, 'depense_cats': depense_cats})


def delete_depense_cat(request, pk):
    depense_cats = get_object_or_404(CategorieDepense, pk=pk)
    if request.method == 'POST':
        depense_cats.delete()
        return redirect('depense_cat_list')
    return render(request, 'depense_cats/delete_depense_cat.html', {'depense_cats': depense_cats})


