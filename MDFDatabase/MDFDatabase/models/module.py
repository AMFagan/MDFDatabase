from typing import List, re

from django.db import models

from .choices import Semester, ElectiveOptions, Levels, StaffRoles, Week


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
        'Module', related_name='required_for', blank=True
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

    def pre_requisites(self):
        return self.required_modules.all()

    def successors(self):
        return self.required_for.all()

    def list_pre_requisites(self) -> str:
        return ', '.join(['<a href="%(s)s"> %(s)s</a>' % {'s': m.code} for m in self.pre_requisites()])

    def list_successors(self) -> str:
        return ', '.join(['<a href="%(s)s"> %(s)s</a>' % {'s': m.code} for m in self.successors()])

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

    def __str__(self) -> str:
        return "%s : %s" % (self.code, self.name)

    def as_tree_pres(self) -> List[str]:
        out = ["--> %s: %s<br><br>" % (self.code, self.name)]
        for subtree in self.pre_requisites():
            out += ['&emsp;' + str(s) for s in subtree.as_tree_pres()]
        return out

    def as_tree_succs(self) -> List[str]:
        out = ["--> %s: %s<br><br>" % (self.code, self.name)]
        for subtree in self.successors():
            out += ['&emsp;' + str(s) for s in subtree.as_tree_succs()]
        return out

    def as_tree_string(self) -> str:
        return '\n'.join(self.as_tree_pres())

    def iterable_assessments(self):
        out = []
        for e in sorted(self.exam_set.all(), key=lambda x: Semester(x.semester).label):
            d = []
            d.append('Examination')
            d.append('Duration')
            d.append(e.duration)
            d.append('Weighting %0.2f%%' % e.weight)
            d.append('Semester ' + Semester(e.semester).label)
            d.append('Week ' + Week(e.week).label if e.week != 'E' else Week(e.week).label)
            out += [d]
        i = 1
        for c in sorted(self.coursework_set.all(), key=lambda x: Semester(x.semester).label):
            d = []
            d.append('Coursework')
            d.append('Number')
            d.append(i)
            d.append('Weighting %0.2f%%' % c.weight)
            d.append('Semester ' + c.semester)
            d.append('Week ' + Week(c.week).label if c.week != 'E' else Week(c.week).label)
            out += [d]
            i += 1
        i = 1
        for p in sorted(self.project_set.all(), key=lambda x: Semester(x.semester).label):
            d = []
            d.append('Project')
            d.append('Number')
            d.append(i)
            d.append('Weighting %0.2f%%' % p.weight)
            d.append('Semester ' + p.semester)
            d.append('Week ' + Week(p.week).label if p.week != 'E' else Week(p.week).label)
            out += [d]
            i += 1
        return out

    def semesters(self):
        out = {'1': {
            '1': [], '2': [], '3': [], '4': [],
            '5': [], '6': [], '7': [], '8': [],
            '9': [], '10': [], '11': [], 'E': [],
            },
            '2': {
                '1': [], '2': [], '3': [], '4': [],
                '5': [], '6': [], '7': [], '8': [],
                '9': [], '10': [], '11': [], 'E': [],
            },
            '3': {
                '1': [], '2': [], '3': [], '4': [],
                '5': [], '6': [], '7': [], '8': [],
                '9': [], '10': [], '11': [], 'E': [],
            },
        }
        for coursework in self.coursework_set.all():
            out[coursework.semester][coursework.week] += [coursework.simple_str()]
        for project in self.project_set.all():
            out[project.semester][project.week] += [project.simple_str()]
        for exam in self.exam_set.all():
            out[exam.semester][exam.week] += [exam.simple_str()]
        for level in out:
            for week in out[level]:
                out[level][week] = "<br/>".join(out[level][week])
        return self.code, out

    def semester_printable(self):
        return Semester(self.semester).label

    def elective_printable(self):
        return ElectiveOptions(self.elective).label
