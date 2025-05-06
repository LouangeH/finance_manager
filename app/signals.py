from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Revenu, RevenuPDF
from views.generate_pdf import generate_pdf_for_revenu

@receiver(post_save, sender=Revenu)
def create_revenu_pdf(sender, instance, created, **kwargs):
    if created:
        pdf_file = generate_pdf_for_revenu(instance)
        RevenuPDF.objects.create(revenu=instance, fichier_pdf=pdf_file)
