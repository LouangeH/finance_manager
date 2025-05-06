#generate_pdf.py

from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from django.core.files.base import ContentFile

def generate_pdf_for_revenu(revenu):
    html_string = render_to_string('revenues/revenu_pdf_template.html', {'revenu': revenu})
    pdf_io = BytesIO()
    HTML(string=html_string).write_pdf(pdf_io)
    return ContentFile(pdf_io.getvalue(), name=f"revenu_{revenu.id}.pdf")


from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from app.models import Revenu, Depense

def revenu_pdf_view(request, revenu_id):
    revenu = Revenu.objects.get(pk=revenu_id)
    html_string = render_to_string('revenues/revenu_pdf_template.html', {'revenu': revenu})

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="revenu_{revenu.id}.pdf"'
    return response

def depense_pdf_view(request, depense_id):
    depense = Depense.objects.get(pk=depense_id)
    html_string = render_to_string('depenses/depense_pdf_template.html', {'depense': depense})

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="depense_{depense.id}.pdf"'
    return response
