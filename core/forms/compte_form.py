from django import forms
from core.models import Compte

class CompteForm(forms.ModelForm):
    class Meta:
        model = Compte
        fields = '__all__'