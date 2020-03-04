from typing import List

from django.db import models

from .choices import Semester, ElectiveOptions, Levels, StaffRoles


class Module(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    credits = models.IntegerField(default=20)
    semester = models.TextField(max_length=1, choices=Semester.choices)
    elective = models.TextField(max_length=1, choices=ElectiveOptions.choices)
    level = models.TextField(max_length=1, choices=Levels.choices)
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
        return ', '.join(['%s (%s)' % (a.assignee.full_name(), StaffRoles(a.role).label)
                          for a in self.assignment_set.all()
                          if a.role != StaffRoles.REGISTRAR])

    def registrars(self) -> str:
        return ', '.join([a.assignee.full_name()
                          for a in self.assignment_set.all()
                          if a.role == StaffRoles.REGISTRAR])

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

    def semesters(self):
        out = {'1': {
            '1': [], '2': [], '3': [], '4': [],
            '5': [], '6': [], '7': [], '8': [],
            '9': [], '10': [], '11': [], '12': [],
            'E': []
        },
            '2': {
                '1': [], '2': [], '3': [], '4': [],
                '5': [], '6': [], '7': [], '8': [],
                '9': [], '10': [], '11': [], '12': [],
                'E': []
            },
            '3': {
                '1': [], '2': [], '3': [], '4': [],
                '5': [], '6': [], '7': [], '8': [],
                '9': [], '10': [], '11': [], '12': [],
                'E': []
            },
        }
        for coursework in self.coursework_set.all():
            out[coursework.semester][coursework.week] += [coursework]
        for project in self.project_set.all():
            out[project.semester][project.week] += [project]
        for exam in self.exam_set.all():
            out[exam.semester][exam.week] += [exam]
        return out




