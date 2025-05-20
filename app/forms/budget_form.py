# # # forms.py
# # # from django import forms
# # # from app.models import BudgetMensuel
# # # from django.utils import timezone

# # # class BudgetMensuelForm(forms.ModelForm):
# # #     class Meta:
# # #         model = BudgetMensuel
# # #         fields = ['mois', 'categorie', 'montant_planifie', 'type', 'objectif', 'prioritaire']
# # #         widgets = {
# # #             'mois': forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}),
# # #             'categorie': forms.Select(attrs={'class': 'form-control'}),
# # #             'montant_planifie': forms.NumberInput(attrs={'class': 'form-control'}),
# # #             'type': forms.Select(attrs={'class': 'form-control'}),
# # #             'objectif': forms.TextInput(attrs={'class': 'form-control'}),
# # #             'prioritaire': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
# # #         }

# # from django import forms
# # from app.models import BudgetMensuel
# # from datetime import datetime

# # class BudgetMensuelForm(forms.ModelForm):
# #     class Meta:
# #         model = BudgetMensuel
# #         fields = ['mois', 'categorie', 'montant_planifie', 'type', 'objectif', 'prioritaire']
# #         widgets = {
# #             'mois': forms.DateInput(attrs={
# #                 'type': 'month',
# #                 'class': 'form-control',
# #                 'min': datetime.now().strftime('%Y-%m')
# #             }),
# #             'categorie': forms.Select(attrs={'class': 'form-control'}),
# #             'montant_planifie': forms.NumberInput(attrs={'class': 'form-control'}),
# #             'type': forms.Select(attrs={'class': 'form-control'}),
# #             'objectif': forms.TextInput(attrs={'class': 'form-control'}),
# #             'prioritaire': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
# #         }

# #     # def clean_mois(self):
# #     #     mois = self.cleaned_data.get('mois')
# #     #     if isinstance(mois, str):  # si navigateur envoie une chaîne (ex: 2025-06)
# #     #         try:
# #     #             mois = datetime.strptime(mois, '%Y-%m').date()
# #     #         except ValueError:
# #     #             raise forms.ValidationError("Format de date invalide (attendu AAAA-MM)")
# #     #     return mois

# #     def clean_mois(self):
# #         mois = self.data.get('mois')  # prendre la valeur brute
# #         try:
# #             mois_date = datetime.strptime(mois, '%Y-%m').date().replace(day=1)
# #         except ValueError:
# #             raise forms.ValidationError("Le format du mois est invalide. Veuillez utiliser AAAA-MM.")
# #         return mois_date

# from django import forms
# from app.models import BudgetMensuel
# from datetime import datetime, date

# class BudgetMensuelForm(forms.ModelForm):
#     class Meta:
#         model = BudgetMensuel
#         fields = ['mois', 'categorie', 'montant_planifie', 'type', 'objectif', 'prioritaire']
#         widgets = {
#             'mois': forms.TextInput(attrs={
#                 'type': 'month',
#                 'class': 'form-control',
#                 'min': datetime.today().strftime('%Y-%m')
#             }),
#             'categorie': forms.Select(attrs={'class': 'form-control'}),
#             'montant_planifie': forms.NumberInput(attrs={'class': 'form-control'}),
#             'type': forms.Select(attrs={'class': 'form-control'}),
#             'objectif': forms.TextInput(attrs={'class': 'form-control'}),
#             'prioritaire': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()

#         # ✅ corriger date type=month (format AAAA-MM → date)
#         mois_str = self.data.get('mois')
#         try:
#             mois_date = datetime.strptime(mois_str, "%Y-%m").date().replace(day=1)
#         except Exception:
#             raise forms.ValidationError("Le format du mois est invalide. Utilisez le sélecteur AAAA-MM.")

#         cleaned_data['mois'] = mois_date

#         # ✅ Vérifier qu’un budget similaire existe déjà
#         categorie = cleaned_data.get('categorie')
#         if mois_date and categorie:
#             exists = BudgetMensuel.objects.filter(mois=mois_date, categorie=categorie).exists()
#             if exists and not self.instance.pk:
#                 raise forms.ValidationError("Un budget existe déjà pour cette catégorie et ce mois.")

#         return cleaned_data

from django import forms
from app.models import BudgetMensuel
from datetime import datetime, date

class BudgetMensuelForm(forms.ModelForm):
    mois = forms.CharField(label="Mois", widget=forms.TextInput(attrs={
        'type': 'month',
        'class': 'form-control',
        'min': datetime.today().strftime('%Y-%m')
    }))

    class Meta:
        model = BudgetMensuel
        fields = ['mois', 'categorie', 'montant_planifie', 'type', 'objectif', 'prioritaire']
        widgets = {
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'montant_planifie': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'objectif': forms.TextInput(attrs={'class': 'form-control'}),
            'prioritaire': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        mois_str = self.data.get('mois')
        try:
            # convertir "2025-06" → date(2025, 6, 1)
            mois_date = datetime.strptime(mois_str, "%Y-%m").date().replace(day=1)
        except ValueError:
            raise forms.ValidationError("Le mois est invalide. Utilisez le format AAAA-MM.")

        # mettre à jour le champ nettoyé
        cleaned_data['mois'] = mois_date

        # vérifie les doublons
        categorie = cleaned_data.get('categorie')
        if mois_date and categorie:
            exists = BudgetMensuel.objects.filter(mois=mois_date, categorie=categorie)
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise forms.ValidationError("Un budget existe déjà pour cette catégorie et ce mois.")

        return cleaned_data
