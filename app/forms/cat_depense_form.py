from django import forms
from app.models import CategorieDepense

class CategorieDepenseForm(forms.ModelForm):
    class Meta:
        model = CategorieDepense
        fields = ['categorie']