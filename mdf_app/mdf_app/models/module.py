from typing import List, re

from django.db import models

from .choices import Semester, ElectiveOptions, Levels, StaffRoles, Week


class Module(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    credits = models.IntegerField(default=20)
    semester = models.TextField(max_length=1, choices=Semester.choices)
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
    resit = models.TextField(default='', blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    passmark = models.IntegerField(default=40)
    elective_boolean = models.BooleanField(default=False, verbose_name='Available as Elective')
    
    class Meta:
        ordering = ['code']

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
        return ', '.join(['<a href="../%(s)s"> %(s)s</a>' % {'s': m.code} for m in self.pre_requisites()])

    def list_successors(self) -> str:
        return ', '.join(['<a href="../%(s)s"> %(s)s</a>' % {'s': m.code} for m in self.successors()])

    def staff(self):
        out = {}
        for a in self.duty_set.all():
            name = a.assignee.full_name()
            if name not in out:
                out[name] = []
            out[name] += [a.role]
        return out

    def other_staff(self) -> str:
        return ', '.join(['%s (%s)' % (a.assignee.full_name(), StaffRoles(a.role).label)
                          for a in self.duty_set.all()
                          if a.role != StaffRoles.REGISTRAR])

    def registrars(self) -> str:
        return ', '.join([a.assignee.full_name()
                          for a in self.duty_set.all()
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
            d.append('Weighting %g%%' % e.weight)
            d.append('Semester ' + Semester(e.semester).label)
            d.append('Week ' + Week(e.week).label if e.week != 'E' else Week(e.week).label)
            out += [d]
        i = 1
        for c in sorted(self.coursework_set.all(), key=lambda x: Semester(x.semester).label):
            d = []
            d.append('Coursework')
            d.append('Number')
            d.append(i)
            d.append('Weighting %g%%' % c.weight)
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
            d.append('Weighting %gf%%' % p.weight)
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

    def class_schedule(self):
        o = self.semesters()
        o = o[1]
        for s in list(o.keys()):
            occupied = False
            for w in o[s]:
                if o[s][w]:
                    occupied = True
            if not occupied:
                del o[s]
        
        out = {'Week': {k: "Semester " + k for k in o},
            '1': {k: [] for k in o}, '2': {k: [] for k in o}, '3': {k: [] for k in o}, '4': {k: [] for k in o},
            '5': {k: [] for k in o}, '6': {k: [] for k in o}, '7': {k: [] for k in o}, '8': {k: [] for k in o},
            '9': {k: [] for k in o}, '10': {k: [] for k in o}, '11': {k: [] for k in o}, 'E': {k: [] for k in o},}
        for s in o:
            for w in o[s]:
                out[w][s] = o[s][w]
                
        
        return out
                
    
    def elective(self):
        coe = [False for option in list(ElectiveOptions)]
        for mem in self.coursemembership_set.all():
            i = 0
            for option in ElectiveOptions:
                if mem.elective == option:
                    coe[i] = True
                i += 1
        out = ''
        i=0
        for option in ElectiveOptions:
            if coe[i]:
                out = out + option.label[0]
            i += 1
        if self.elective_boolean:
            out = out + 'E'
        return out

    def semester_printable(self):
        return Semester(self.semester).label

    def elective_printable(self):
        return self.elective()

    def get_duties(self):
        order = {'1':'1', '5':'2', '2':'3', '3':'4', '4':'5'}
        out = self.duty_set.all()
        return sorted(out, key=lambda d: order[d.role])
        
    def total_duty(self):
        out = []
        lec, tut, lab, ove = 0, 0, 0, 0,
        for d in self.get_duties():
            lec = lec + d.lecture_hours
            tut = tut + d.tutorial_hours
            lab = lab + d.lab_hours
            ove = ove + d.overhead_hours
        out.append(str(lec))
        out.append(str(tut))
        out.append(str(lab))
        out.append(str(ove))
        return out
        
        