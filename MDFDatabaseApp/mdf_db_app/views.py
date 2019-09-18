from django.shortcuts import get_object_or_404


from mdf_db_app.models import Module, Staff, Course

# Create your views here.

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
#import weasyprint as weas
import tempfile


def mdf_test(request, code):
    module = get_object_or_404(Module, code=code)
    response = HttpResponse(render_to_string('mdf.xhtml', {'module': module}))
    #html = weas.HTML(string=render_to_string('mdf.xhtml', {'module': module}))
    #result = html.write_pdf()

    # Creating http response
    #response = HttpResponse(result, content_type='application/pdf;')


    return response


def module_index(request):
    entries = Module.objects.order_by('level', 'code')
    return HttpResponse(render_to_string('module_index.xhtml', {'entries': entries}))


def staff_index(request):
    entries = Staff.objects.order_by('id_number')
    return HttpResponse(render_to_string('staff_index.xhtml', {'entries': entries}))


def staff_member(request, id_number):
    staff = get_object_or_404(Staff, id_number=id_number)
    assignments = staff.assignment_set.all()
    return HttpResponse(render_to_string('staff_page.xhtml', {'staff': staff, 'assignments': assignments}))


def course_index(request):
    entries = Course.objects.all()
    return HttpResponse(render_to_string('course_index.xhtml', {'entries': entries}))

def course(request, level, shorthand):
    c = get_object_or_404(Course, award=level, shorthand=shorthand)
    return HttpResponse(render_to_string('course_page.xhtml', {'course': c, 'levels': c.levels()}))