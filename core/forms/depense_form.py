from django import forms
from core.models import Depense

class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = '__all__'