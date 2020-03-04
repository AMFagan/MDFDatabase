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
                out[mem.level] = mem.module.semesters()
                continue
            sems = mem.module.semesters()
            #print('%s %s' % (mem.module, sems)) # Def have module
            for semester in sems:
                #print(sems[semester])
                for week in sems[semester]:
                    #print('##%s##\n{{%s}}' % (out[mem.level][semester][week], sems[semester][week]))
                    out[mem.level][semester][week] += sems[semester][week]


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
    level = models.TextField(max_length=1, choices=Levels.choices)
    elective = models.TextField(max_length=1, choices=ElectiveOptions.choices)

    def __str__(self):
        return "%s students can take %s in year %s (%s)" % (self.course, self.module, self.level, self.elective)

