from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.forms import LoginForm, RegisterForm
from app.models import UserProfile

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_list(request):
    user = UserProfile.objects.all()
    return render(request, 'accounts/user_list.html', {'user': user})



#@login_required
def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def edit_user(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)
    form = RegisterForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('fuel_sale_list')
    
    return render(request, 'accounts/create_user.html', {'form': form, 'user': user})

@login_required
def delete_user(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('fuel_sale_list')
    return render(request, 'accounts/delete_user.html', {'user': user})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
