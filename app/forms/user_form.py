from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=100)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Peux-tu m'aider a integrer une pour faire la budgetisation annuel et il va me fournir un budget mensuel realiste et applicable pour me permettre a atteindre le budget annuel? explique-moi comment le faire? 
