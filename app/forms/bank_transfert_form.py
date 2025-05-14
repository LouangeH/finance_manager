# from django import forms
# from app.models import BankTransfert

# class BankTransfertForm(forms.ModelForm):
#     class Meta:
#         model = BankTransfert
#         fields = ['banque_source', 'banque_destination', 'montant', 'motif']

#     def clean(self):
#         cleaned_data = super().clean()
#         source = cleaned_data.get('banque_source')
#         montant = cleaned_data.get('montant')
#         destination = cleaned_data.get('banque_destination')

#         # Vérifie que la banque source et destination sont différentes
#         if source and destination and source == destination:
#             raise forms.ValidationError("La banque source et la banque destination doivent être différentes.")


#         if source and montant:
#             from django.db.models import Sum
#             operations = source.bank.all()
#             total_depot = operations.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
#             total_retrait = operations.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
#             total_tenue = operations.filter(type_operation='tenue').aggregate(Sum('montant'))['montant__sum'] or 0

#             solde = total_depot - total_retrait - total_tenue

#             if montant > solde:
#                 raise forms.ValidationError(f"Solde insuffisant sur la banque source ({solde:,.0f} FBu disponibles).")
#         return cleaned_data
from django import forms
from django.db.models import Sum
from app.models import BankTransfert, CategorieBank  # adapte le chemin selon ton app

class BankTransfertForm(forms.ModelForm):
    class Meta:
        model = BankTransfert
        fields = ['banque_source', 'banque_destination', 'montant', 'motif']

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('banque_source')
        destination = cleaned_data.get('banque_destination')
        montant = cleaned_data.get('montant')

        if source and destination and source == destination:
            raise forms.ValidationError("La banque source et la banque destination doivent être différentes.")

        if source and montant:
            operations = source.bank.all()
            total_depot = operations.filter(type_operation='depot').aggregate(Sum('montant'))['montant__sum'] or 0
            total_retrait = operations.filter(type_operation='retrait').aggregate(Sum('montant'))['montant__sum'] or 0
            total_tenue = operations.filter(type_operation='tenue').aggregate(Sum('montant'))['montant__sum'] or 0

            solde = total_depot - total_retrait - total_tenue

            if montant > solde:
                raise forms.ValidationError(
                    f"Solde insuffisant sur la banque source ({solde:,.0f} FBu disponibles)."
                )

        return cleaned_data
