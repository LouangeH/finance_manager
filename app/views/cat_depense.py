from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.models import CategorieDepense
from app.forms import CategorieDepenseForm
from django.core.paginator import Paginator

#@login_required
def cat_depense_list(request):
    cat_depenses = CategorieDepense.objects.all()
    paginator = Paginator(cat_depenses, 10)  # 10 achats par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'depenses/cat_depense_list.html', {'cat_depenses': cat_depenses, 'page_obj': page_obj})


#@login_required
def create_cat_depense(request):
    form = CategorieDepenseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cat_depense_list')
    return render(request, 'depenses/create_cat_depense.html', {'form': form})


#@login_required
def update_cat_depense(request, pk):
    cat_depenses = get_object_or_404(CategorieDepense, pk=pk)
    form = CategorieDepenseForm(request.POST or None, instance=cat_depenses)
    if form.is_valid():
        form.save()
        return redirect('cat_depense_list')
    return render(request, 'depenses/create_cat_depense.html', {'form': form})


#@login_required
def delete_cat_depense(request, pk):
    cat_depenses = get_object_or_404(CategorieDepense, pk=pk)
    if request.method == 'POST':
        cat_depenses.delete()
        return redirect('cat_depense_list')
    return render(request, 'depenses/confirm_delete.html', {'cat_depenses': cat_depenses})
