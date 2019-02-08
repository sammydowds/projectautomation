from django.db import models


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Project(models.Model):
    projectnumber = models.IntegerField()
    projectname = models.CharField(max_length=100)
    mechanicalrelease = models.DateField(blank=True, null = True)
    mechanicalreleasecomplete = models.BooleanField(default=False)
    electricalrelease = models.DateField(blank=True, null = True)
    electricalreleasecomplete = models.BooleanField(default=False)
    manufacturing = models.DateField(blank=True, null = True)
    manufacturingcomplete = models.BooleanField(default=False)
    finishing = models.DateField(blank=True, null = True)
    finishingcomplete = models.BooleanField(default=False)
    assembly = models.DateField(blank=True, null = True)
    assemblycomplete = models.BooleanField(default=False)
    integration = models.DateField(blank=True, null = True)
    integrationcomplete = models.BooleanField(default=False)
    internalrunoff = models.DateField(blank=True, null = True)
    internalrunoffcomplete = models.BooleanField(default=False)
    customerrunoff = models.DateField(blank=True, null = True)
    customerrunoffcomplete = models.BooleanField(default=False)
    ship = models.DateField(blank=True, null = True)
    shipcomplete = models.BooleanField(default=False)
    installstart = models.DateField(blank=True, null = True)
    installstartcomplete = models.BooleanField(default=False)
    installfinish = models.DateField(blank=True, null = True)
    installfinishcomplete = models.BooleanField(default=False)
    documentation = models.DateField(blank=True, null = True)
    documentationcomplete = models.BooleanField(default=False)
    offtrack = models.BooleanField(blank=True, null = True)
    onwatch = models.BooleanField(blank=True, null = True)
    iscurrent = models.BooleanField(blank=True, null = True)
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.projectname



class InitialProject(models.Model):
    projectnumber = models.IntegerField()
    projectname = models.CharField(max_length=100)
    mechanicalrelease = models.DateField(null = True)
    electricalrelease = models.DateField(null = True)
    manufacturing = models.DateField(null = True)
    finishing = models.DateField(null = True)
    assembly = models.DateField(null = True)
    integration = models.DateField(null = True)
    internalrunoff = models.DateField(null = True)
    customerrunoff = models.DateField(null = True)
    ship = models.DateField(null = True)
    installstart = models.DateField(null = True)
    installfinish = models.DateField(null = True)
    documentation = models.DateField(null = True)
    offtrack = models.BooleanField(null = True)
    onwatch = models.BooleanField(null = True)
    iscurrent = models.BooleanField(null = True)
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.projectname
