from datetime import *
from dateutil.relativedelta import relativedelta
from django.db import models
from projects.models import *
import json
import operator

#pulls projects by department and analyzes dates in each of the 12 months of the year
#returns: 2 dictionaries = 1) {Phase: list(project number, project name, start date, end date)}, 2) {Phase: list({month: #of projects})}
#TODO add days in between milestones to Dictionary 1
#TODO add check if date is None
def capacity_analysis():

    #creating dictionary of phases with list of projects and dates -------------------
    capacity_company = {}
    projects = Project.objects.all()
    capacity_company["Engineering"] = list(projects.filter(Electrical_Release__gte = datetime.today()).values_list('projectnumber', 'projectname', 'engineering_start', 'Mechanical_Release', 'Electrical_Release').order_by('Mechanical_Release'))
    capacity_company["Manufacturing_and_Finishing"] = list(projects.filter(Finishing__gte = datetime.today()).values_list('projectnumber', 'projectname', 'Mechanical_Release', 'Manufacturing', 'Finishing').order_by('Manufacturing'))
    capacity_company["Assembly"] = list(projects.filter(Assembly__gte = datetime.today()).values_list('projectnumber', 'projectname', 'Finishing', 'Assembly').order_by('Finishing'))
    capacity_company["Integration_at_Acieta"] = list(projects.filter(Internal_Runoff__gte = datetime.today()).values_list('projectnumber', 'projectname', 'Assembly', 'Internal_Runoff').order_by('Assembly'))
    capacity_company["Install_at_Customer"] = list(projects.filter(Install_Finish__gte = datetime.today()).values_list('projectnumber', 'projectname', 'Install_Start', 'Install_Finish').order_by('Install_Start'))
    #----------------------------------------------------------------------------------

    #creating a dict of form - {Phase: list({month: #of projects})}
    capacity_analysis = {}

    #looping through the departments of the company
    for k,v in capacity_company.items():
        #creating phase meta
        capacity_analysis[k] = None
        #creating an empty list to be appended dictionaries of each month to
        months = {}
        for i in range(0, 12):
            date = datetime.today() + relativedelta(months=i)
            date = date.year, date.month, 1
            months[date] = 0
        #looping through the projects in the phase
        for project in v:
            months_accounted_for = []
            for date in project:
                #filtering out values that are not dates

                if date != None and not isinstance(date, int) and not isinstance(date, str) and not datetime.today().date() > date:
                    #checking if we have already accounted for the month
                    if (date.year, date.month) not in months_accounted_for:
                        #updating count of projects during this month
                        dt = date.year, date.month, 1
                        months[dt] = months[dt] + 1
                        months_accounted_for.append((date.year, date.month))
        test_dict = {}
        for month in months:
            test_dict[''.join([str(month[0]), str(month[1]), str(month[2])])] = months[month]
        capacity_analysis[k] = list(test_dict.items())

                    #if the month is equal to the dates month append it to the monthly analysis dict
    return capacity_company, capacity_analysis

#returns a dictionary of suggested dates for tasks with key = description of task, values =  date, and assumption/comment
#TODO add milestones to this mix
# def suggest_schedule(project):
#     suggested_sched = {}
#
#     return sorted_dict_sugg_sched, gantt_data_suggested

def organize_tasks(projects_dict):
    list_all_tasks = []
    for project in projects_dict:
        #creating ordered list of dates and descriptions
        for k, v in project.items():
            item = [v[0], v[1], k]
            # if v[0] >= date.today():
            list_all_tasks.append(item)

    sorted_tasks = sorted(list_all_tasks)
    sorted_tasks = dict((z, [x, y]) for x, y, z in sorted_tasks)

    return sorted_tasks
