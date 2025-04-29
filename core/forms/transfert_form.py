from django import forms
from core.models import TransfertFonds

class TransfertFondsForm(forms.ModelForm):
    class Meta:
        model = TransfertFonds
        fields = '__all__'