from django import forms
from app.models import CategorieBank

class CategorieBankForm(forms.ModelForm):
    class Meta:
        model = CategorieBank
        fields = ['categorie']