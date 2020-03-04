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
        return "%s Assessment S%sW%s" % (self.module.code, self.semester, self.week)


class Exam(Assessment):
    duration = models.IntegerField()

    def __str__(self):
        return super().__str__().replace('Assessment', 'Exam')


class Coursework(Assessment):

    def __str__(self):
        return super().__str__().replace('Assessment', 'Coursework')


class Project(Assessment):

    def __str__(self):
        return super().__str__().replace('Assessment', 'Project')
