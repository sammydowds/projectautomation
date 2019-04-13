from django.db import models
from datetime import date
import numpy as np
from django.contrib.auth.models import User


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Project(models.Model):
    projectnumber = models.IntegerField()
    projectname = models.CharField(max_length=100)
    engineering_start = models.DateField(blank=True, null = True)
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
    offtrack = models.BooleanField(default=True, null = True)
    onwatch = models.BooleanField(default=True, null = True)
    iscurrent = models.BooleanField(default=True, null = True)
    projectmanager = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)


    def __str__(self):
        return self.projectname

    #return dictionary of milestones in the projects
    def milestones(self):

        #convert object to list of tuples
        proj = list(self.__dict__.items())
        milestones=[]
        milestones.append(proj[4])
        for i in range(4, 29):
            if i % 2 != 0:
                #saving milestone
                milestones.append(proj[i])
        #dictionary of milestones only
        return dict(milestones)


    #returns dictionary of remaining milestones
    def milestones_remaining(self):

        #converting query to dictionary
        project_dash = self.__dict__

        #appending purely milestones without status into a variable
        milestones = []

        #convert attributes to list of tuples
        proj_dash = list(project_dash.items())

        this_milestone = []
        duration = []
        for i in range(4, 29):
            if i % 2 != 0 and proj_dash[i+1][1] == False:
                #saving milestone
                milestones.append(proj_dash[i])
                #saving previous milestone before
                this_milestone.append(proj_dash[i][0])

        return dict(milestones)

    #returns milestone currently on
    def current_milestone(self):
        #first milestone appended is the next milestone
        this_milestone = list(self.milestones_remaining())
        return this_milestone[0]

    #returning the current phase project and the progress as a percentage
    def current_phase(self):

        #finding the phase based on the current milestone
        phases = self.phase_durations()
        today = date.today()
        status = {}
        #looping through and finding which range of dates for a phase we are in
        for k, v in phases.items():
            print(v[1])
            print(v[2])
            if today >= v[1] and today <= v[2]:
                status['Phase'] = k
                print(self.busdays_between(today, v[1]))
                status['Progress'] = int(round(self.busdays_between(today, v[1])/v[0] * 100))
                break
        print(status)
        return status


    #return dictionary of business days between milestones
    def milestone_durations(self):
        milestones = list(self.milestones().items())
        milestone_durations = {}
        for i in range(1, len(milestones)):
            milestone_durations[milestones[i][0]] = self.busdays_between(milestones[i][1], milestones[i-1][1]),milestones[i-1][1],milestones[i][1]
        return milestone_durations


    #returns dictionary of business days between phases, along with the beginning date and end date
    #return phase = (business days, start, finish)
    def phase_durations(self):
        milestone_dur = list(self.milestone_durations().items())
        phase_durations = {}

        for i in range(0, len(milestone_dur)):
            if i == 0:
                phase_durations['Engineering'] = milestone_dur[i+1][1][0] + milestone_dur[i][1][0], milestone_dur[i][1][1], milestone_dur[i+1][1][2]
            if i == 6:
                phase_durations['Run-Off Period'] = milestone_dur[i+1][1][0] + milestone_dur[i][1][0], milestone_dur[i][1][1], milestone_dur[i+1][1][2]
            if i == 9:
                phase_durations['Installation'] = milestone_dur[i+1][1][0], milestone_dur[i][1][1], milestone_dur[i+1][1][2]
            if i == 8:
                phase_durations['Preparing to Ship'] = milestone_dur[i][1][0], milestone_dur[i-1][1][1], milestone_dur[i][1][2]
                phase_durations['Shipment In Transit'] = milestone_dur[i+1][1][0], milestone_dur[i][1][1], milestone_dur[i+1][1][2]
            elif i > 1 and i < 6 or i == 11:
                phase_durations[milestone_dur[i][0]] = milestone_dur[i][1][0], milestone_dur[i][1][1], milestone_dur[i][1][2]
        return(phase_durations)


    #returns business days between two dates
    def busdays_between(self, date1, date2):
        #TODO Create case for 0 business days between
        return np.busday_count(date2,date1)









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
