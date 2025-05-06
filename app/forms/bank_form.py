from django import forms
from app.models import BankOperation

class BankOperationForm(forms.ModelForm):
    class Meta:
        model = BankOperation
        fields = ['bank','type_operation', 'montant', 'motif']
    
    def clean(self):
        cleaned_data = super().clean()
        type_operation = cleaned_data.get('type_operation')
        montant = cleaned_data.get('montant')

        if not montant or not type_operation:
            return cleaned_data

        from app.models import BankOperation, Revenu, Depense
        from django.db.models import Sum

        # Solde caisse actuel
        revenus = Revenu.objects.aggregate(Sum('somme'))['somme__sum'] or 0
        retraits = BankOperation.objects.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
        depots = BankOperation.objects.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
        depenses = Depense.objects.aggregate(Sum('somme'))['somme__sum'] or 0

        solde_caisse = (revenus + retraits) - (depots + depenses)

        # Validation pour retrait
        if type_operation == 'retrait':
            from django.db.models import Sum
            bank = cleaned_data.get('bank')
            if bank:
                operations = bank.bank.all()
                total_depots = operations.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
                total_retraits = operations.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
                total_tenue = operations.filter(type_operation='tenue').aggregate(Sum('montant'))['montant__sum'] or 0
                solde_banque = total_depots - total_retraits - total_tenue

                if montant > solde_banque:
                    raise forms.ValidationError(
                        f"Retrait invalide : solde insuffisant ({solde_banque:,.0f} FBu disponibles pour cette banque)."
                    )

        # Validation pour dépôt
        if type_operation == 'depot':
            if montant > solde_caisse:
                raise forms.ValidationError(
                    f"Dépôt invalide : la caisse ne contient que {solde_caisse:,.0f} FBu."
                )

        return cleaned_data
    
    
