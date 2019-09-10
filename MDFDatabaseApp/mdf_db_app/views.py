from django.shortcuts import get_object_or_404
from mdf_db_app.models import Module

# Create your views here.

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint as weas
import tempfile


def mdf_test(request, code):
    module = get_object_or_404(Module, code=code)
    html = weas.HTML(string=render_to_string('mdf.xhtml', {'module': module}))
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')


    return response
