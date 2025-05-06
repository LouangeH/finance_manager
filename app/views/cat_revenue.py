from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.models import CategorieRevenue
from app.forms import CategorieRevenueForm
from django.core.paginator import Paginator

@login_required
def cat_revenue_list(request):
    cat_revenues = CategorieRevenue.objects.all()
    paginator = Paginator(cat_revenues, 10)  # 10 achats par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'revenues/cat_revenue_list.html', {'cat_revenues': cat_revenues, 'page_obj': page_obj})


@login_required
def create_cat_revenue(request):
    form = CategorieRevenueForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cat_revenue_list')
    return render(request, 'revenues/create_cat_revenue.html', {'form': form})


@login_required
def update_cat_revenue(request, pk):
    cat_revenues = get_object_or_404(CategorieRevenue, pk=pk)
    form = CategorieRevenueForm(request.POST or None, instance=cat_revenues)
    if form.is_valid():
        form.save()
        return redirect('cat_revenue_list')
    return render(request, 'revenues/create_cat_revenue.html', {'form': form})


@login_required
def delete_cat_revenue(request, pk):
    cat_revenues = get_object_or_404(CategorieRevenue, pk=pk)
    if request.method == 'POST':
        cat_revenues.delete()
        return redirect('cat_revenue_list')
    return render(request, 'revenues/confirm_delete.html', {'cat_revenues': cat_revenues})
