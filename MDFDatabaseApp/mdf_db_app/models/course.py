from django.db import models
from . import Module, levels, elective_options
#from django_mysql.models import EnumField


class Course(models.Model):
    name = models.CharField(max_length=100)
    award = models.CharField(max_length=10)
    shorthand = models.CharField(max_length=5, default='')

    def __str__(self):
        return "%s %s" % (self.award, self.name)

    def full_shorthand(self):
        return "%s_%s" % (self.award, self.shorthand)

    def levels(self):
        out = {}
        for mem in self.coursemembership_set.all():
            if mem.level not in out:
                out[mem.level] = mem.module.semesters()
                continue
            for semester in mem.module.semesters():
                for week in semester:
                    out[mem.mem.level][semester][week] += semester[week]
        for ls in list(out.keys()):
            for sem in list(out[ls].keys()):
                i = 0
                for w in out[ls][sem]:
                    i += len(out[ls][sem][w])
                if i == 0:
                    del out[ls][sem]
        return out


class CourseMembership(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    level = models.CharField(max_length=1)
    elective = models.CharField(max_length=2)

    def __str__(self):
        return "%s students can take %s in year %s (%s)" % (self.course, self.module, self.level, self.elective)
