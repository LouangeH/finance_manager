from django.shortcuts import render, redirect, get_object_or_404
from app.forms import DepenseForm
from app.models import Depense, CategorieDepense
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.utils.timezone import datetime

#@login_required
def depense_list(request):
    depenses = Depense.objects.all().order_by('-date')

    type_id = request.GET.get('type')
    if type_id:
        depenses = depenses.filter(depense_id=type_id)

    periode = request.GET.get('periode')
    if periode:
        try:
            annee, mois = map(int, periode.split('-'))
            depenses = depenses.filter(date__year=annee, date__month=mois)
        except ValueError:
            pass

    total_filtre = depenses.aggregate(Sum('somme'))['somme__sum'] or 0

    # pagination (optionnel)
    from django.core.paginator import Paginator
    paginator = Paginator(depenses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'depenses': page_obj,
        'page_obj': page_obj,
        'categories': CategorieDepense.objects.all(),
        'total_filtre': total_filtre,
        'current_year': datetime.today().year,
        'current_month': str(datetime.today().month).zfill(2),
    }
    return render(request, 'depenses/depense_list.html', context)

#@login_required
def create_depense(request):
    form = DepenseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('depense_list')
    return render(request, 'depenses/create_depense.html', {'form': form})

#@login_required
def edit_depense(request, pk):
    depenses = get_object_or_404(Depense, pk=pk)
    form = DepenseForm(request.POST or None, instance=depenses)
    if form.is_valid():
        form.save()
        return redirect('depense_list')
    
    return render(request, 'depenses/create_depense.html', {'form': form, 'depenses': depenses})

#@login_required
def delete_depense(request, pk):
    depenses = get_object_or_404(Depense, pk=pk)
    if request.method == 'POST':
        depenses.delete()
        return redirect('depense_list')
    return render(request, 'depenses/delete_depense.html', {'depenses': depenses})