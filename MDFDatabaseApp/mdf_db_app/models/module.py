from typing import List

from django_mysql.models import EnumField
from django.db import models

semesters = (
    '1', '1/2', '2', '2/3', '3', '3/1', '1/2/3',
)

levels = (
        '1', '2', '3', '4', '5',
    )
elective_options = (
        'NE', 'PE', 'EO',
    )

class Module(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    credits = models.IntegerField(default=20)
    semester = EnumField(choices=semesters, default='1/2')
    elective = EnumField(choices=elective_options, default='NE')
    level = EnumField(choices=levels, default='1')
    aims = models.TextField(default='', blank=True)
    learning_outcomes = models.TextField(default='', blank=True)
    syllabus = models.TextField(default='', blank=True)
    criteria = models.TextField(default='', blank=True)
    feedback = models.TextField(default='', blank=True)
    comments = models.TextField(default='', blank=True)
    reading = models.TextField(default='', blank=True)
    required_modules = models.ManyToManyField(
        'Module', related_name='requirements', blank=True
    )
    lecture_hours = models.IntegerField(default=0)
    tutorial_hours = models.IntegerField(default=0)
    assignment_hours = models.IntegerField(default=0)
    lab_hours = models.IntegerField(default=0)
    study_hours = models.IntegerField(default=0)

    def total_hours(self) -> int:
        return (0
                + self.lecture_hours
                + self.tutorial_hours
                + self.assignment_hours
                + self.lab_hours
                + self.study_hours
                )

    def list_pre_requisites(self) -> str:
        return ', '.join([m.code for m in self.required_modules.all()])

    def staff(self):
        out = {}
        for a in self.assignment_set.all():
            name = a.assignee.full_name()
            if name not in out:
                out[name] = []
            out[name] += [a.role]
        return out

    def other_staff(self) -> str:
        return ', '.join(['%s (%s)' % (a.assignee.full_name(), a.role)
                          for a in self.assignment_set.all()
                          if a.role != 'Class Registrar'])

    def registrars(self) -> str:
        return ', '.join([a.assignee.full_name()
                          for a in self.assignment_set.all()
                          if a.role == 'Class Registrar'])

    def __str__(self) -> str: return "%s : %s" % (self.code, self.name)

    def as_tree(self) -> List[str]:
        out = [self.code]
        for subtree in self.required_modules.all():
            out += ['- - > ' + str(s) for s in subtree.as_tree()]
        return out

    def as_tree_string(self) -> str:
        return '\n'.join(self.as_tree())

    def iterable_assessments(self):
        out = []
        for e in self.exam_set.all():
            d = []
            d.append('Examination')
            d.append('Duration')
            d.append(e.duration)
            d.append('Weighting (%)')
            d.append(e.weight)
            d.append('S')
            d.append(e.semester)
            d.append('W')
            d.append(e.week)
            out += [d]
        i = 1
        for c in self.coursework_set.all():
            d = []
            d.append('Coursework')
            d.append('Number')
            d.append(i)
            d.append('Weighting (%)')
            d.append(c.weight)
            d.append('S')
            d.append(c.semester)
            d.append('W')
            d.append(c.week)
            out += [d]
            i += 1
        i = 1
        for p in self.project_set.all():
            d = []
            d.append('Project')
            d.append('Number')
            d.append(i)
            d.append('Weighting (%)')
            d.append(p.weight)
            d.append('S')
            d.append(p.semester)
            d.append('W')
            d.append(p.week)
            out += [d]
            i += 1
        return out



