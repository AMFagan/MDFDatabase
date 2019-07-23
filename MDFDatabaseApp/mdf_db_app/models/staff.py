from django.db import models
from django_mysql.models import EnumField
from . import Module

ROLES = (
    'Class Registrar',
    'Lecturer',
    'Marker',
    'Assistant',
)


class Staff(models.Model):
    id_number = models.IntegerField(unique=True)
    forename = models.TextField()
    surname = models.TextField()

    def __str__(self):
        return "%s %s (%s)" % (self.forename, self.surname, self.id_number)


class Assignment(models.Model):
    assignee = models.ForeignKey(Staff, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    role = EnumField(choices=ROLES)
    hours = models.IntegerField()

    def __str__(self):
        return "%s assigned to %s as %s" % (str(self.assignee), self.module.code, self.role)

