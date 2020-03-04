from django.http import Http404
from django.shortcuts import get_object_or_404
from openpyxl import load_workbook
from . import Module


def batch_upload(filename: str):
    wb = load_workbook(filename=filename)
    for sheet in wb.worksheets:
            for line in sheet.iter_rows(2, values_only=True):
                if not line[0]:
                    continue
                try:
                    m = get_object_or_404(Module, code = str(line[0] or ''))
                except Http404 as e:
                    m = Module()
                    m.code = str(line[0] or '')
                m.name = str(line[1] or '')
                m.credits = str(line[2] or 0)
                m.semester = str(line[3] or '1/2')
                m.elective = str(line[4] or 'NE')
                m.level = str(line[5] or '1')
                m.aims = str(line[6] or '')
                m.learning_outcomes = str(line[7] or '')
                m.syllabus = str(line[8] or '')
                m.criteria = str(line[9] or '')
                m.feedback = str(line[10] or '')
                m.comments = str(line[11] or '')
                m.reading = str(line[12] or '')
                m.lecture_hours = str(line[14] or 0)
                m.tutorial_hours = str(line[15] or 0)
                m.assignment_hours = str(line[16] or 0)
                m.lab_hours = str(line[17] or 0)
                m.study_hours = str(line[18] or 0)
                m.save()
                for req in str(line[13] or '').split(','):
                    if req == '':
                        continue
                    #print('adding reqs')
                    code = req.strip()
                    try:
                        m.required_modules.add(get_object_or_404(Module, code=code))
                    except Http404 as e:
                        newm = Module()
                        newm.code = code
                        newm.save()
                        m.required_modules.add(newm)
                m.save()
    wb.close()
