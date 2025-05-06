from django import forms
from app.models import Depense

class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = ['depense', 'description','somme']

    def clean(self):
        cleaned_data = super().clean()
        somme = cleaned_data.get('somme')

        if somme:
            from app.models import Revenu, BankOperation, Depense
            from django.db.models import Sum

            revenus = Revenu.objects.aggregate(Sum('somme'))['somme__sum'] or 0
            retraits = BankOperation.objects.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
            depenses = Depense.objects.aggregate(Sum('somme'))['somme__sum'] or 0
            depots = BankOperation.objects.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0

            solde_caisse = (revenus + retraits) - (depenses + depots)

            if somme > solde_caisse:
                raise forms.ValidationError(
                    f"Dépense invalide : la caisse actuelle ne contient que {solde_caisse:,.0f} FBu."
                )
