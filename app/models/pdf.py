from django.db import models

class RevenuPDF(models.Model):
    revenu = models.OneToOneField('Revenu', on_delete=models.CASCADE)
    fichier_pdf = models.FileField(upload_to='pdfs/revenus/')
    date_created = models.DateTimeField(auto_now_add=True)

class DepensePDF(models.Model):
    depense = models.OneToOneField('Depense', on_delete=models.CASCADE)
    fichier_pdf = models.FileField(upload_to='pdfs/depenses/')
    date_created = models.DateTimeField(auto_now_add=True)
