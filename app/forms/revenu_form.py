from django import forms
from app.models import Revenu

class RevenuForm(forms.ModelForm):
    class Meta:
        model = Revenu
        fields = ['revenu', 'source', 'somme']