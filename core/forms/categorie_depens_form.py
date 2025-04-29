from django import forms
from core.models import CategorieDepense

class CategorieDepenseForm(forms.ModelForm):
    class Meta:
        model = CategorieDepense
        fields = '__all__'