from django.db import models
#from django_mysql.models import EnumField
from . import Module

ROLES = (
    'Class Registrar',
    'Lecturer',
    'Assistant',
    'Marker',
)


class Staff(models.Model):
    id_number = models.IntegerField(unique=True)
    title = models.CharField(max_length=10, blank=True, default='')
    forename = models.TextField()
    surname = models.TextField()

    def full_name(self):
        return " ".join(filter(lambda x: x,
                               [self.title, self.forename, self.surname]))

    def __str__(self):
        return (
                "%s (%s)" %
                (self.full_name(), self.id_number)
        )


class Assignment(models.Model):
    assignee = models.ForeignKey(Staff, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    role = models.CharField(max_length=15)
    hours = models.IntegerField()

    class Meta:
        unique_together = ('assignee', 'module')

    def __str__(self):
        return (
                "%s assigned to %s as %s for %s hours" %
                (str(self.assignee), self.module.code, self.role, self.hours)
        )

    def code(self):
        return self.module.code
