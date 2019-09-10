from django.db import models
from . import Module, levels, elective_options
from django_mysql.models import EnumField


class Course(models.Model):
    name = models.CharField(max_length=100)
    award = models.CharField(max_length=10)

    def __str__(self):
        return "%s %s" % (self.award, self.name)


class CourseMembership(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    level = EnumField(choices=levels)
    elective = EnumField(choices=elective_options)

    def __str__(self):
        return "%s students can take %s in year %s (%s)" % (self.course, self.module, self.level, self.elective)
