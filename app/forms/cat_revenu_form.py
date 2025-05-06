from django import forms
from app.models import CategorieRevenue

class CategorieRevenueForm(forms.ModelForm):
    class Meta:
        model = CategorieRevenue
        fields = ['categorie']