from django.db import models
from . import Module
from .choices import Semester, ReducedSemester, Week


class Assessment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester = models.TextField(max_length=1, choices=ReducedSemester)
    week = models.TextField(max_length=2, choices=Week.choices)
    weight = models.FloatField(default=0.0)
    information = models.TextField()

    def save(self, *args, **kwargs):
        self.module.save()
        super(Assessment, self).save(*args, **kwargs)

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
        return "Exam %g%%" % (self.weight)

class Coursework(Assessment):

    class Meta:
        verbose_name = "Coursework"
        verbose_name_plural = verbose_name

    def __str__(self):
        return super().__str__().replace('Assessment', 'Coursework')

    def simple_str(self):
        return "CW %g%%" % (self.weight)

class Project(Assessment):

    def __str__(self):
        return super().__str__().replace('Assessment', 'Project')

    def simple_str(self):
        return "Project %g%%" % (self.weight)