from django.shortcuts import render, redirect, get_object_or_404
from core.forms import RevenueForm
from core.models import Revenue
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def revenue_list(request):
    revenues = Revenue.objects.all().order_by('-date')
    paginator = Paginator(revenues, 10)  # 10 achats par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'revenues/revenue_list.html', {'page_obj': page_obj, 'revenues': revenues})


def create_revenue(request):
    form = RevenueForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('revenue_list')
    return render(request, 'revenues/create_revenue.html', {'form': form})


def edit_revenue(request, pk):
    revenues = get_object_or_404(Revenue, pk=pk)
    form = RevenueForm(request.POST or None, instance=revenues)
    if form.is_valid():
        form.save()
        return redirect('revenue_list')
    
    return render(request, 'revenues/create_revenue.html', {'form': form, 'revenues': revenues})


def delete_revenue(request, pk):
    revenues = get_object_or_404(Revenue, pk=pk)
    if request.method == 'POST':
        revenues.delete()
        return redirect('revenue_list')
    return render(request, 'revenues/delete_revenue.html', {'revenues': revenues})


