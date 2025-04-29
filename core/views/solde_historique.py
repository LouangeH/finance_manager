from django.shortcuts import render
from core.models import HistoriqueSolde
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def solde_list(request):
    soldes = HistoriqueSolde.objects.all().order_by('-date')
    paginator = Paginator(soldes, 10)  # 10 achats par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'soldes/solde_list.html', {'page_obj': page_obj, 'soldes': soldes})
