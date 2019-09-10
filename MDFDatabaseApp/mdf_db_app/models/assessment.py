from django.db import models
from . import Module

from django_mysql.models import EnumField


class Assessment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester = EnumField(choices=('1', '2', '3'),
                         default='2')
    week = EnumField(choices=tuple(str(i) for i in range(1, 13)) + ('E',),
                     default='E'
                     )
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
