from django.shortcuts import get_object_or_404
from mdf_app.models import Module, Course, Staff

# Create your views here.

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
# import weasyprint as weas
import tempfile

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def mdf_test(request, code):
    module = get_object_or_404(Module, code=code)
    # html = weas.HTML(string=render_to_string('mdf.xhtml', {'module': module}))
    # result = html.write_pdf()

    # Creating http response
    response = HttpResponse(
        render_to_string('mdf.xhtml', {'module': module, 'schedule':module.class_schedule()}))  # result, content_type='application/pdf;')

    return response

def mdf_pdf(request, code):
    module = get_object_or_404(Module, code=code)
    # html = weas.HTML(string=render_to_string('mdf.xhtml', {'module': module}))
    # result = html.write_pdf()

    # Creating http response
    response = render_to_pdf('mdf-pdf.xhtml', {'module': module})

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
    entries = Staff.objects.order_by('surname')
    return HttpResponse(render_to_string('staff_index.xhtml', {'entries': entries}))

def all_staff_surname(request):
    entries = Staff.objects.order_by('surname')
    return HttpResponse(render_to_string('all_staff.xhtml', {'entries': entries}))
    
def all_staff_hours(request):
    entries = Staff.objects.all()
    entries = sorted(entries, key=lambda s: s.absolute_total(), reverse=True)
    return HttpResponse(render_to_string('all_staff.xhtml', {'entries': entries}))

def staff_member(request, personnel_id):
    staff = get_object_or_404(Staff, personnel_id=personnel_id)
    duties = staff.duty_set.all()
    admin = staff.administrativeduty_set.all()
    return HttpResponse(render_to_string('staff_page.xhtml', {'staff': staff, 'duties': duties, 'admin': admin}))


def course_index(request):
    entries = Course.objects.all()
    return HttpResponse(render_to_string('course_index.xhtml', {'entries': entries}))


def course(request, code):
    c = get_object_or_404(Course, id=code)
    return HttpResponse(render_to_string('course_page.xhtml', {'course': c, 'levels': c.all_classes()}))

def course_schedule(request, code):
    c = get_object_or_404(Course, id=code)
    return HttpResponse(render_to_string('course_schedule.xhtml', {'course': c, 'levels': c.levels()}))

def course_year(request, code, year):
    c = get_object_or_404(Course, id=code)
    return HttpResponse(render_to_string('course_year.xhtml', {'course': c, 'mems': c.get_level(year), 'year': year}))

def dependancies(request, code):
    module = get_object_or_404(Module, code=code)
    response = HttpResponse(render_to_string('dependancy.xhtml', {'module': module, 'list': module.as_tree_pres()}))
    return response


def successors(request, code):
    module = get_object_or_404(Module, code=code)
    response = HttpResponse(render_to_string('dependancy.xhtml', {'module': module, 'list': module.as_tree_succs()}))
    return response

def duties_module(request, code):
    module = get_object_or_404(Module, code=code)
    response = HttpResponse(render_to_string('duty.xhtml', {'module': module}))
    return response
    
def duty_index(request):
    modules = {'1':[],'2':[],'3':[],'4':[],'5':[],'9':[]}
    for m in Module.objects.all():
        modules[m.level] += [m]
    for i in list(modules.keys()):
        if len(modules[i]) == 0:
            del modules[i]
    response = HttpResponse(render_to_string('all_duties.xhtml', {'modules': modules}))
    return response

def home(request):
    return HttpResponse(render_to_string('home.xhtml', {}))