from datetime import *
from dateutil.relativedelta import relativedelta
from django.db import models
from projects.models import *
import json

#pulls projects by department and analyzes dates in each of the 12 months of the year
#returns: 2 dictionaries = 1) {Phase: list(project number, project name, start date, end date)}, 2) {Phase: list({month: #of projects})}
def capacity_analysis():

    #creating dictionary of phases with list of projects and dates -------------------
    capacity_company = {}
    projects = Project.objects.all()
    capacity_company["Engineering"] = list(projects.filter(electricalrelease__gte = datetime.today()).values_list('projectnumber', 'projectname', 'engineering_start', 'mechanicalrelease', 'electricalrelease').order_by('mechanicalrelease'))
    capacity_company["Manufacturing_and_Finishing"] = list(projects.filter(finishing__gte = datetime.today()).values_list('projectnumber', 'projectname', 'mechanicalrelease', 'manufacturing', 'finishing').order_by('manufacturing'))
    capacity_company["Assembly"] = list(projects.filter(assembly__gte = datetime.today()).values_list('projectnumber', 'projectname', 'finishing', 'assembly').order_by('finishing'))
    capacity_company["Integration_at_Acieta"] = list(projects.filter(internalrunoff__gte = datetime.today()).values_list('projectnumber', 'projectname', 'assembly', 'internalrunoff').order_by('assembly'))
    capacity_company["Install_at_Customer"] = list(projects.filter(installfinish__gte = datetime.today()).values_list('projectnumber', 'projectname', 'installstart', 'installfinish').order_by('installstart'))
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
            print(month)
        capacity_analysis[k] = list(test_dict.items())

                    #if the month is equal to the dates month append it to the monthly analysis dict

    print(capacity_analysis)





    return capacity_company, capacity_analysis
