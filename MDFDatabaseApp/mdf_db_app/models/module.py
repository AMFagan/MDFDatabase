from django_mysql.models import EnumField
from django.db import models


class Module(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    credits = models.IntegerField(default=20)
    semester = EnumField(choices=(
        '1', '1/2', '2', '2/3', '3', '3/1', '1/2/3',
    ))
    elective = EnumField(choices=(
        'NE', 'PE', 'EO',
    ))
    level = EnumField(choices=(
        '1', '2', '3', '4', '5',
    ))
    aims = models.TextField(default='', blank=True)
    syllabus = models.TextField(default='', blank=True)
    comments = models.TextField(default='', blank=True)
    reading = models.TextField(default='', blank=True)
    required_modules = models.ManyToManyField('Module', related_name='requirements', blank=True)
    total_hours = models.IntegerField(default=0)
    lecture_hours = models.IntegerField(default=0)
    tutorial_hours = models.IntegerField(default=0)
    assignment_hours = models.IntegerField(default=0)
    lab_hours = models.IntegerField(default=0)
    study_hours = models.IntegerField(default=0)

    def __str__(self):
        return "%s : %s" % (self.code, self.name)
