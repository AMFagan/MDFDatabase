from django.db import models
from . import Module
from .choices import StaffRoles


class Staff(models.Model):
    personnel_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=10, blank=True, default='')
    salutation = models.TextField()
    forename = models.TextField()
    surname = models.TextField()
    email = models.TextField()
    job_title = models.TextField()
    
    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = verbose_name
        ordering = ['surname']

    def full_name(self):
        return " ".join(filter(lambda x: x,
                               [self.title, self.salutation, self.surname]))

    def __str__(self):
        return self.full_name()
        #(
        #        "%s (%s)" %
        #        (self.full_name(), self.id_number)
        #)

    def get_duties(self):
        return self.duty_set.all()
        
    def get_admins(self):
        return self.administrativeduty_set.all()
        
    def total_duty(self):
        out = []
        lec, tut, lab, ove = 0, 0, 0, 0,
        for d in self.get_duties():
            lec = lec + d.lecture_hours
            tut = tut + d.tutorial_hours
            lab = lab + d.lab_hours
            ove = ove + d.overhead_hours
        for d in self.administrativeduty_set.all():
            ove = ove + d.hours
        out.append(lec)
        out.append(tut)
        out.append(lab)
        out.append(ove)
        return out
        
    def absolute_total(self):
        return sum(self.total_duty())
    
    def update(self):
        import pyodbc 
        conn = pyodbc.connect( 'Driver={SQL Server};'
                              'Server=ENG-AENEA;'
                              'Database=FOE;'
                              'UID=mdf-app;'
                              'PWD=kuwuca-34;'
                              )
           
        cursor = conn.cursor()

        q = cursor.execute("SELECT [cntPersonnelId]"
                           ",[strTitle]"
                           ",[strSalutation]"
                           ",[strForename]"
                           ",[strSurname]"
                           ",[strJobTitle]"
                           ",[strEmailAddress]"
                           ",[lngPersonID]"
                           "FROM [FOE].[MDF].[vtblPersonnel]"
                           "WHERE [cntPersonnelId] = " + str(self.personell_id))
                           
        item = q.fetchone()
        
        self.personnel_id = item[0]
        self.title = item[1]
        self.salutation = item[2]
        self.forename = item[3]
        self.surname = item[4]
        self.email = item[5]
        self.job_title = item[5]
        self.save()

class Duty(models.Model):
    assignee = models.ForeignKey(Staff, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    role = models.TextField(max_length=1, choices=StaffRoles.choices)
    lecture_hours = models.IntegerField()
    tutorial_hours = models.IntegerField()
    lab_hours = models.IntegerField()
    overhead_hours = models.IntegerField()
    
    def save(self, *args, **kwargs):
        self.module.save()
        super(Duty, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('assignee', 'module')
        verbose_name = "Duty"
        verbose_name_plural = "Duties"

    def __str__(self):
        return (
                "%s assigned to %s as %s" %
                (str(self.assignee), self.module.code, StaffRoles.choices[int(self.role)-1][1])
        )

    def code(self):
        return self.module.code
        
    def role_str(self):
        return StaffRoles.choices[int(self.role)-1][1]
        
    def total_duty(self):
        return self.lecture_hours + self.tutorial_hours + self.lab_hours + self.overhead_hours
        
class AdministrativeDuty(models.Model):
    assignee = models.ForeignKey(Staff, on_delete=models.CASCADE)
    code = models.CharField(default = '', max_length=5, unique=True)
    hours = models.IntegerField(default = 0)
    description = models.TextField(default='', blank=True)
    
    class Meta:
        verbose_name = "Administrative Duty"
        verbose_name_plural = "Administrative Duties"

    def __str__(self):
        return (
                "%s administrative role (%s)" %
                (str(self.assignee), self.code or "null")
        )
