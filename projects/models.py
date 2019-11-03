from django.db import models
from datetime import date, datetime, timedelta
import numpy as np
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES = (
        ("offtrack", "Off Track"),
        ("onwatch","On Watch"),
        ("onhold","On Hold"),
        ("update", "Update"),
        ("ontrack", "On Track")

    )
    projectnumber = models.IntegerField(unique=True)
    projectname = models.TextField()
    Comments = models.CharField(max_length=255, default="Enter Project Comments.", null = True)
    engineering_start = models.DateField(blank=True, null = True)
    Mechanical_Release = models.DateField('Mech Rel', blank=True, null = True)
    Mechanical_Release_Complete = models.BooleanField(default=False)
    Mechanical_Release_Scheduled = models.BooleanField(default=False)
    Electrical_Release = models.DateField('Electrical Release', blank=True, null = True)
    Electrical_Release_Complete = models.BooleanField(default=False)
    Electrical_Release_Scheduled = models.BooleanField(default=False)
    Manufacturing = models.DateField(blank=True, null = True)
    Manufacturing_Complete = models.BooleanField(default=False)
    Manufacturing_Scheduled = models.BooleanField(default=False)
    Finishing = models.DateField(blank=True, null = True)
    Finishing_Complete = models.BooleanField(default=False)
    Finishing_Scheduled = models.BooleanField(default=True)
    Assembly = models.DateField(blank=True, null = True)
    Assembly_Complete = models.BooleanField(default=False)
    Assembly_Scheduled = models.BooleanField(default=False)
    Internal_Runoff = models.DateField(blank=True, null = True)
    Internal_Runoff_Complete = models.BooleanField(default=False)
    Internal_Runoff_Scheduled = models.BooleanField(default=False)
    Customer_Runoff = models.DateField(blank=True, null = True)
    Customer_Runoff_Complete = models.BooleanField(default=False)
    Customer_Runoff_Scheduled = models.BooleanField(default=False)
    Ship = models.DateField(blank=True, null = True)
    Ship_Complete = models.BooleanField(default=False)
    Ship_Scheduled = models.BooleanField(default=False)
    Install_Start = models.DateField(blank=True, null = True)
    Install_Start_Complete = models.BooleanField(default=False)
    Install_Start_Scheduled = models.BooleanField(default=False)
    Install_Finish = models.DateField(blank=True, null = True)
    Install_Finish_Complete= models.BooleanField(default=False)
    Install_Finish_Scheduled= models.BooleanField(default=False)
    Documentation = models.DateField(blank=True, null = True)
    Documentation_Complete = models.BooleanField(default=False)
    Documentation_Scheduled = models.BooleanField(default=False)
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="offtrack", null = True)
    iscurrent = models.BooleanField(default=True, null = True)
    projectmanager = models.ForeignKey(User, blank=True, null=True, on_delete = models.SET_NULL)
    mechanicalengineer = models.CharField(max_length=20, default="Not Entered", null = True)
    electricalengineer = models.CharField(max_length=20, default="Not Entered", null = True)
    programmer = models.CharField(max_length=20, default="Not Entered", null = True)
    lastupdated = models.DateField(default = datetime(2015, 10, 21), null = True)
    Slippage = models.IntegerField(default=0)

    def __str__(self):
        return self.projectname

    #return dictionary of milestones in the projects
    #data structure of return: {'Milestone_Name': {'start': datetime, 'end': datetime, 'duration':, int}....}
    def milestones(self):

        #listing out which attributes are milestones. Note: could make this customizable and expandable if projects do not fit this mold in the future (create a separate class?)
        list_milestones = ['engineering_start', \
        'Mechanical_Release',\
        'Electrical_Release', \
        'Manufacturing',\
        'Finishing',\
        'Assembly',\
        'Internal_Runoff', \
        'Customer_Runoff', \
        'Ship', \
        'Install_Start', \
        'Install_Finish', \
        'Documentation', \
        ]


        #storing project to dictionary and creating new empty dict
        dict_project = self.__dict__
        dict_milestones = {}

        for i in range(1,len(list_milestones)):
            #start date is previous milestone date
            start = dict_project[list_milestones[i-1]]
            #end date is current milestone date in the list
            end = dict_project[list_milestones[i]]
            #duration between both start and end dates
            duration = self.busdays_between(end, start)
            #status of the milestone
            status = dict_project[list_milestones[i]+ '_Complete']
            #status of the milestone
            scheduled = dict_project[list_milestones[i] + '_Scheduled']
            print(scheduled)
            print(list_milestones[i])
            #storing information to dictionary
            dict_milestones[list_milestones[i]] = {'start': start, 'end': end, 'duration': duration, 'status': status, 'scheduled': scheduled}

        return dict_milestones


    #milestones this week for project
    #returns dict with project number, name, and list of milestones happening this week
    def thisweek(self):

        #saving project to dict
        this_project = self.__dict__

        #saving this week number
        if datetime.today().isocalendar()[2] < 6:
            week = datetime.today().isocalendar()[1]
        else:
            week = datetime.today().isocalendar()[1] + 1

        #storing milestones this week of a project
        milestones_this_week = {}

        #working through each field - checking if it is within this week
        for milestone, value in this_project.items():
            if isinstance(value, date) and milestone != 'lastupdated':
                if (value.isocalendar()[1]) == week:
                    milestones_this_week.update({milestone: {'end': value}})

        #appending some meta data
        this_week = {"projectnumber": self.projectnumber, "projectname": self.projectname, "milestonesweek": milestones_this_week}

        return this_week

    #returns milestone currently on in form of dict = {'name': str of name, 'start': datetime, 'end': datetime, 'duration': int, 'days_until': int}
    def current_milestone(self):

        #first milestone appended is the next milestone
        project = self.milestones()
        # TODO change to central time or time of laptop?
        today = date.today()
        milestone = {}

        #looping through project milestones
        for key, value in project.items():
            if value['status'] == False and value['end'] != None:
                value['days_until'] = self.busdays_between(value['end'], today)
                value['name'] = key
                return value

        #if date is in the past or no dates exits
        if milestone == {}:
            milestone = {'name': 'Review Dates', 'start': None, 'end': None, 'duration': None, 'days_until': None, 'scheduled': False}
            return milestone

    #checking if a milestone has been complete in one of the projects
    def anymilestonescomplete(self):
        project = self.milestones()
        for milestone, values in project.items():
            if values['status'] == True:
                return True
        return False
    #data structure of return: {'current_phase': str of phase name,'start':, 'end':, 'progress': int of % progress}
    def current_phase(self):

        #finding the phase based on the current milestone
        phases = self.phases()
        del phases['Project']
        today = date.today()
        status = {}

        #looping through phases and their calculated info
        for phase, info in phases.items():

            #ensuring all dates are entered
            if info['start'] != None and info['end'] != None and info['duration'] != None:
                start = info['start']
                end = info['end']
                duration = info['duration']
                if today <= end:
                    status['current_phase'] = phase
                    status['start'] = info['start']
                    status['end'] = info['end']

                    #if duration is equal to 0, then mark progress as 100%
                    if info['duration'] != 0:
                        percent_complete = int(round((self.busdays_between(today, start)/duration)*100))

                        #checking if milestone is - % complete, if so it means the milestone is in the future
                        if percent_complete >= 0:
                            status['progress'] = percent_complete
                            break
                        else:
                            status['progress'] = 0
                            break
                    else:
                        status['progress'] = 100
                        break
            #setting phase to unknown if there are no dates entered for all values
            else:
                return {'current_phase': None, 'start': None, 'end': None, 'progress': 0}

        return status

    #returns business days between two dates
    def busdays_between(self, date1, date2):
        #TODO Create case for 0 business days between
        if isinstance(date1, date) and isinstance(date2, date):
            return np.busday_count(date2,date1)
        else:
            return("[ERROR: Need Dates To Calc]")

class InitialProject(models.Model):
    STATUS_CHOICES = (
        ("offtrack", "Off Track"),
        ("onwatch","On Watch"),
        ("onhold","On Hold"),
        ("update", "Update"),

    )
    projectnumber = models.IntegerField()
    projectname = models.CharField(max_length=100)
    Mechanical_Release = models.DateField(null = True)
    Electrical_Release = models.DateField(null = True)
    Manufacturing = models.DateField(null = True)
    Finishing = models.DateField(null = True)
    Assembly = models.DateField(null = True)
    Integration = models.DateField(null = True)
    Internal_Runoff = models.DateField(null = True)
    Customer_Runoff = models.DateField(null = True)
    Ship = models.DateField(null = True)
    Install_Start = models.DateField(null = True)
    Install_Finish= models.DateField(null = True)
    Documentation = models.DateField(null = True)
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="offtrack", null = True)
    iscurrent = models.BooleanField(default=True, null = True)
    projectmanager = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)
    lastupdated = models.DateField(default = datetime(2015, 10, 21), null = True)
    # employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.projectname
