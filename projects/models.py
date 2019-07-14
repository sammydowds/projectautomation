from django.db import models
from datetime import date, datetime, timedelta
import numpy as np
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField




# # Create your models here.
# class Employee(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.EmailField()
#
#     def __str__(self):
#         return self.name

class Project(models.Model):
    STATUS_CHOICES = (
        ('offtrack', 'Off Track'),
        ('onwatch','On Watch'),
        ('onhold','On Hold'),
        ('update', 'Update')
    )
    projectnumber = models.IntegerField()
    projectname = models.TextField()
    engineering_start = models.DateField(blank=True, null = True)
    Mechanical_Release = models.DateField(blank=True, null = True)
    Electrical_Release = models.DateField(blank=True, null = True)
    Manufacturing = models.DateField(blank=True, null = True)
    Finishing = models.DateField(blank=True, null = True)
    Assembly = models.DateField(blank=True, null = True)
    Integration = models.DateField(blank=True, null = True)
    Internal_Runoff = models.DateField(blank=True, null = True)
    Customer_Runoff = models.DateField(blank=True, null = True)
    Ship = models.DateField(blank=True, null = True)
    Install_Start = models.DateField(blank=True, null = True)
    Install_Finish = models.DateField(blank=True, null = True)
    Documentation = models.DateField(blank=True, null = True)
    Status = ArrayField(models.CharField(max_length=10, choices=STATUS_CHOICES, default='offtrack', null = True))
    iscurrent = models.BooleanField(default=True, null = True)
    projectmanager = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)
    lastupdated = models.DateField(default = datetime(2015, 10, 21), null = True)


    def __str__(self):
        return self.projectname

    def progress(self):
        if self.Documentation and self.engineering_start:
            return round(100-(int(self.busdays_between(date.today(), self.Documentation))/int(self.busdays_between(self.engineering_start, self.Documentation)))*100, 0)
        else:
            return 0

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
        'Integration',\
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
            #storing information to dictionary
            dict_milestones[list_milestones[i]] = {'start': start, 'end': end, 'duration': duration}

        return dict_milestones

    #data structure of return: {'Phase_name': {'start': datetime, 'end': datetime, 'duration':, int}....}
    def phases(self):

        #listing out which attributes make up a phase in the project. start and finish milestones
        phases = {'Project': ['engineering_start', 'Documentation'], \
        'Mechanical_Engineering': ['engineering_start', 'Mechanical_Release'], \
        'Electrical_Engineering': ['Mechanical_Release', 'Electrical_Release'], \
        'Manufacturing': ['Electrical_Release', 'Finishing'], \
        'Assembly': ['Finishing', 'Assembly'], \
        'Integration': ['Assembly', 'Customer_Runoff'], \
        'Installation': ['Install_Start', 'Install_Finish'], \
        'Documentation': ['Install_Finish', 'Documentation'], \
        }

        #saving info to a dict
        project = self.__dict__
        phase_calcs = {}

        #calculating dates and saving to calc dict
        for phase, value in phases.items():
            start = project[value[0]]
            end = project[value[-1]]
            duration = self.busdays_between(end, start)
            phase_calcs[phase] = {'start': start, 'end': end, 'duration': duration, 'hours': duration*8}

        return phase_calcs

    #data structure in (future): {'Task_name': ['Deadline Milestone', int of lead time in weeks, int of duration it takes]}
    #data structure of return: {'Task_name': {'start': datetime, 'end': datetime, 'duration':, int}.....}
    def suggested_tasks(self):

        #format of tasks: name of task, deadline, start date, lead time(weeks), duration(days)
        tasks = {'Transition Meeting': ['Mechanical_Release', 4, 2],\
        'Mechanical Design Intent Meeting': ['Mechanical_Release', 3, 2],\
        'Risk Assessment': ['Mechanical_Release', 3, 2],\
        'Mechanical Design Review': ['Mechanical_Release', 1, 2],\
        'Electrical Design Review': ['Electrical_Release', 1, 2],\
        'Finish SOW': ['Mechanical_Release', 1.5, 10],\
        'Review Outsourcing Plan for Manufacturing': ['Mechanical_Release', -0.5, 5],\
        'Review Manufacturing Work Plans': ['Mechanical_Release', -1, 5],\
        'Send Engineering Invoice': ['Electrical_Release', -0.5, 2],\
        'Order Robot': ['Assembly', 6, 1],\
        'Review Assembly Work Plans': ['Assembly', 3, 5],\
        'Manufacturing/Assembly Transition Meeting': ['Assembly', 1, 1],\
        'Assembly/Integration Transition Meeting': ['Integration', 1, 1],\
        'Prepare for Customer On-Site': ['Customer_Runoff', 1, 2],\
        'Prepare Acieta Run Off Document': ['Customer_Runoff', 0.5, 1],\
        'Prepare Shipping Document': ['Ship', 2, 1],\
        'Send Acieta Run-Off Invoice': ['Ship', -0.1, 1],\
        'Prepare T&E Document': ['Install_Start', 1, 2],\
        'Prepare Final Run-Off Document': ['Install_Finish', 1, 2],\
        'Send Final Run-Off Invoice': ['Install_Finish', -.1, 2],\
        }

        #saving this project to a dictionary
        this_project = self.__dict__
        suggested_schedule= {}
        for task in tasks.items():
            #setting duration, leadtime and deadline of a task
            duration = task[1][2]
            leadtime = task[1][1]
            milestone_deadline = this_project[task[1][0]]

            #testing to see if milestone is none
            if milestone_deadline != None:
                #calculating dates
                start = milestone_deadline - timedelta(weeks=leadtime)
                end = start + timedelta(days=duration)
                #saving task name and info to dictionary
                suggested_schedule[task[0]] = {'start': start, 'end': end, 'duration': duration}
            else:
                #saving None to start and end because there is no date entered for the reference milestone
                suggested_schedule[task[0]] = {'start': None, 'end': None, 'duration': duration}

        return suggested_schedule


    #returns milestone currently on in form of dict = {'name': str of name, 'start': datetime, 'end': datetime, 'duration': int, 'days_until': int}
    def current_milestone(self):

        #first milestone appended is the next milestone
        project = self.milestones()
        today = date.today()
        milestone = {}

        #looping through project milestones
        for key, value in project.items():
            if value['end'] != None:
                value['days_until'] = self.busdays_between(value['end'], today)
                value['name'] = key
                if value['end'] > today:
                    return value

        #if date is in the past or no dates exits
        if milestone == {}:
            milestone = {'name': 'Review Dates', 'start': None, 'end': 'Need to Update', 'duration': None, 'days_until': None}
            return milestone

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
        ('offtrack', 'Off Track'),
        ('onwatch','On Watch'),
        ('onhold','On Hold'),
        ('update', 'Update')
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
    Ship= models.DateField(null = True)
    Install_Start = models.DateField(null = True)
    Install_Finish= models.DateField(null = True)
    Documentation = models.DateField(null = True)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OT')
    iscurrent = models.BooleanField(default=True, null = True)
    projectmanager = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)
    lastupdated = models.DateField(default = datetime(2015, 10, 21), null = True)
    # employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.projectname
