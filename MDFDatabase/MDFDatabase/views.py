from django.shortcuts import get_object_or_404
from MDFDatabase.models import Module, Course, Staff

# Create your views here.

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
# import weasyprint as weas
import tempfile


def mdf_test(request, code):
    module = get_object_or_404(Module, code=code)
    # html = weas.HTML(string=render_to_string('mdf.xhtml', {'module': module}))
    # result = html.write_pdf()

    # Creating http response
    response = HttpResponse(
        render_to_string('mdf.xhtml', {'module': module}))  # result, content_type='application/pdf;')

    return response


def module_index(title, request):
    entries = Module.objects.order_by('level', 'code')
    return HttpResponse(render_to_string('module_index.xhtml', {'title': title, 'entries': entries}))


def mdf_index(request):
    return module_index("MDF Index", request)


def pre_index(request):
    return module_index("Pre Requisite Index", request)


def succ_index(request):
    return module_index("Successor Index", request)


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


def dependancies(request, code):
    module = get_object_or_404(Module, code=code)
    response = HttpResponse(render_to_string('dependancy.xhtml', {'module': module, 'list': module.as_tree_pres()}))
    return response


def successors(request, code):
    module = get_object_or_404(Module, code=code)
    response = HttpResponse(render_to_string('dependancy.xhtml', {'module': module, 'list': module.as_tree_succs()}))
    return response


def home(request):
    return HttpResponse(render_to_string('home.xhtml', {}))