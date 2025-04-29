from django.shortcuts import render, redirect, get_object_or_404
from core.forms import ObjectifForm
from core.models import Objectif
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def objectif_list(request):
    objectifs = Objectif.objects.all().order_by('-date')
    paginator = Paginator(objectifs, 10)  # 10 achats par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'objectifs/objectif_list.html', {'page_obj': page_obj, 'objectifs': objectifs})


def create_objectif(request):
    form = ObjectifForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('objectif_list')
    return render(request, 'objectifs/create_objectif.html', {'form': form})


def edit_objectif(request, pk):
    objectifs = get_object_or_404(Objectif, pk=pk)
    form = ObjectifForm(request.POST or None, instance=objectifs)
    if form.is_valid():
        form.save()
        return redirect('objectif_list')
    
    return render(request, 'objectifs/create_objectif.html', {'form': form, 'objectifs': objectifs})


def delete_objectif(request, pk):
    objectifs = get_object_or_404(Objectif, pk=pk)
    if request.method == 'POST':
        objectifs.delete()
        return redirect('objectif_list')
    return render(request, 'objectifs/delete_objectif.html', {'objectifs': objectifs})


