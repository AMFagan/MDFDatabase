from django.db import models
from . import Module

from django_mysql.models import EnumField


class Coursework(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    week = EnumField(choices=
                     tuple(str(i) for i in range(1, 13)) + ('Exam Period',)
                     )
    weight = models.IntegerField(default=0)
    information = models.TextField()

    def __str__(self):
        return "%s Coursework, week %s" % (self.module.code, self.week)


class Exam(Coursework):
    duration = models.IntegerField()

    def __str__(self):
        return "%s Exam, week %s, duration %s" % (self.module.code, self.week, self.duration)


