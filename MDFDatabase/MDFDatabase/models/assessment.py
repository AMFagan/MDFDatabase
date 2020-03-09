from django.db import models
from . import Module
from .choices import Semester, Week


class Assessment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester = models.TextField(max_length=1, choices=Semester.choices)
    week = models.TextField(max_length=2, choices=Week.choices)
    weight = models.IntegerField(default=0)
    information = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return "%s Assessment S: %s W: %s" % (self.module.code, Semester(self.semester).label, Week(self.week).label)

    def simple_str(self):
        return "%s Assessment" % self.module.code


class Exam(Assessment):
    duration = models.IntegerField()

    def __str__(self):
        return super().__str__().replace('Assessment', 'Exam')

    def simple_str(self):
        return "%s Exam" % self.module.code

class Coursework(Assessment):

    def __str__(self):
        return super().__str__().replace('Assessment', 'Coursework')

    def simple_str(self):
        return "%s Coursework" % self.module.code

class Project(Assessment):

    def __str__(self):
        return super().__str__().replace('Assessment', 'Project')

    def simple_str(self):
        return "%s Project" % self.module.code