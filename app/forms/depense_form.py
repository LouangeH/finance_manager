from django import forms
from app.models import Depense, CategorieBank, BankOperation, Revenu
from django.db.models import Sum

class DepenseForm(forms.ModelForm):
    provenance_banque = forms.BooleanField(required=False, label="Effectuer cette dépense via une banque")
    banque_utilisee = forms.ModelChoiceField(
        queryset=CategorieBank.objects.all(),
        required=False,
        label="Banque"
    )

    class Meta:
        model = Depense
        fields = ['depense', 'description', 'somme', 'provenance_banque', 'banque_utilisee']

    def clean(self):
        cleaned_data = super().clean()
        somme = cleaned_data.get('somme')
        use_bank = cleaned_data.get('provenance_banque')
        bank = cleaned_data.get('banque_utilisee')

        if somme is None:
            return cleaned_data

        # Vérifier si la banque est requise mais non sélectionnée
        if use_bank and not bank:
            raise forms.ValidationError("Veuillez sélectionner une banque.")

        # Calcul des soldes
        revenus = Revenu.objects.aggregate(Sum('somme'))['somme__sum'] or 0
        retraits = BankOperation.objects.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
        depots = BankOperation.objects.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
        depenses = Depense.objects.aggregate(Sum('somme'))['somme__sum'] or 0

        solde_caisse = (revenus + retraits) - (depenses + depots)

        if use_bank:
            # Solde spécifique à la banque sélectionnée
            total_depots = bank.bank.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
            total_retraits = bank.bank.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
            total_tenue = bank.bank.filter(type_operation='tenue').aggregate(Sum('montant'))['montant__sum'] or 0

            solde_banque = total_depots - total_retraits - total_tenue

            if somme > solde_banque:
                raise forms.ValidationError(
                    f"Solde insuffisant dans la banque sélectionnée ({solde_banque:,.0f} FBu disponibles)."
                )
        else:
            if somme > solde_caisse:
                raise forms.ValidationError(
                    f"Dépense invalide : la caisse actuelle ne contient que {solde_caisse:,.0f} FBu."
                )

        return cleaned_data
