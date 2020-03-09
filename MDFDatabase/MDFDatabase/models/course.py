from django.db import models
from . import Module
from .choices import Levels, ElectiveOptions

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
            #print(out)
            if mem.level not in out:
                out[mem.level] = {}
            code, sems = mem.module.semesters()
            #print('%s %s' % (mem.module, sems)) # Def have module
            for s in sems:
                if s not in out[mem.level]:
                    out[mem.level][s] = {}
                out[mem.level][s][code] = sems[s]

        for ls in out:
            for sem in list(out[ls].keys()):
                i = 0
                for m in list(out[ls][sem].keys()):
                    j = 0
                    for w in list(out[ls][sem][m].keys()):
                        if out[ls][sem][m][w] != "":
                            i += 1
                            j += 1
                    if j == 0:
                        del out[ls][sem][m]
                if i == 0:
                    del out[ls][sem]
        return out

class CourseMembership(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    level = models.TextField(max_length=1, choices=Levels.choices)
    elective = models.TextField(max_length=1, choices=ElectiveOptions.choices)

    def __str__(self):
        return "%s students can take %s in year %s (%s)" % (self.course, self.module, self.level, self.elective)


def helper(ls):
    for l in ls:
        print("Level " + l)
        for s in ls[l]:
            print("Semester " + s)
            print(ls[l][s])