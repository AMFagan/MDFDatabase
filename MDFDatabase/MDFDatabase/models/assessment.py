from django.db import models
from . import Module
from .choices import Semester, ReducedSemester, Week


class Assessment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester = models.TextField(max_length=1, choices=ReducedSemester)
    week = models.TextField(max_length=2, choices=Week.choices)
    weight = models.FloatField(default=0.0)
    information = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return "%s Assessment S: %s W: %s" % (self.module.code, Semester(self.semester).label, Week(self.week).label)

    def simple_str(self):
        return "%s Assessment" % self.module.code


class Exam(Assessment):
    duration = models.FloatField()

    def __str__(self):
        return super().__str__().replace('Assessment', 'Exam')

    def simple_str(self):
        return "%s Exam (%0.2f%%)" % (self.module.code, self.weight)

class Coursework(Assessment):

    def __str__(self):
        return super().__str__().replace('Assessment', 'Coursework')

    def simple_str(self):
        return "%s Coursework (%0.2f%%)" % (self.module.code, self.weight)

class Project(Assessment):

    def __str__(self):
        return super().__str__().replace('Assessment', 'Project')

    def simple_str(self):
        return "%s Project (%0.2f%%)" % (self.module.code, self.weight)