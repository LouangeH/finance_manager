from django.shortcuts import render, redirect, get_object_or_404
from app.forms import RevenuForm
from app.models import Revenu, CategorieRevenue
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.utils.timezone import datetime

#@login_required
def revenue_list(request):
    revenues = Revenu.objects.all().order_by('-date')

    type_id = request.GET.get('type')
    if type_id:
        revenues = revenues.filter(revenu_id=type_id)

    periode = request.GET.get('periode')
    if periode:
        try:
            annee, mois = map(int, periode.split('-'))
            revenues = revenues.filter(date__year=annee, date__month=mois)
        except ValueError:
            pass

    total_filtre = revenues.aggregate(Sum('somme'))['somme__sum'] or 0

    # pagination (optionnel)
    from django.core.paginator import Paginator
    paginator = Paginator(revenues, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'revenues': page_obj,
        'page_obj': page_obj,
        'categories': CategorieRevenue.objects.all(),
        'total_filtre': total_filtre,
        'current_year': datetime.today().year,
        'current_month': str(datetime.today().month).zfill(2),
    }
    return render(request, 'revenues/revenue_list.html', context)

#@login_required
def create_revenue(request):
    form = RevenuForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('revenue_list')
    return render(request, 'revenues/create_revenue.html', {'form': form})

#@login_required
def edit_revenue(request, pk):
    revenues = get_object_or_404(Revenu, pk=pk)
    form = RevenuForm(request.POST or None, instance=revenues)
    if form.is_valid():
        form.save()
        return redirect('revenue_list')
    
    return render(request, 'revenues/create_revenue.html', {'form': form, 'revenues': revenues})

#@login_required
def delete_revenue(request, pk):
    revenues = get_object_or_404(Revenu, pk=pk)
    if request.method == 'POST':
        revenues.delete()
        return redirect('revenue_list')
    return render(request, 'revenues/delete_revenue.html', {'revenues': revenues})


