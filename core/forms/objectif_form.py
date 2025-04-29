from django import forms
from core.models import Objectif

class ObjectifForm(forms.ModelForm):
    class Meta:
        model = Objectif
        fields = '__all__'