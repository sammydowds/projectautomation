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
def suggest_schedule(project):
    suggested_sched = {}
    proj_name, proj_number = project.projectname, project.projectnumber
    project = project.milestones()

    #TODO Need to check if date is none in here
    gantt_data_suggested = []

    #creating a suggested schedule based on typical process of managing projects at Acieta
    suggested_sched[str(proj_number) + ': ' + 'Mechanical Design Review'] = project['Mechanical_Release'] - timedelta(weeks=1), "1 week is enough time to detail before Mechanical Release, need to send out approvals this day"
    gantt_data_suggested.append(['ME Review', str(project['Mechanical_Release'] - timedelta(days=11)), str(project['Mechanical_Release']- timedelta(days=7))])
    suggested_sched[str(proj_number) + ': ' + 'Electrical Design Review'] = project['Electrical_Release'] - timedelta(weeks=1), "1 week is enough time to detail before Electrical Release, need to send out approvals this day"
    gantt_data_suggested.append(['EE Review', str(project['Electrical_Release'] - timedelta(weeks=1)), str(project['Electrical_Release'])])
    suggested_sched[str(proj_number) + ': ' + 'SOW Finished and Sent to Customer'] = project['Mechanical_Release'] - timedelta(days=7), "Sent at the same time with mechanical approval drawings. No major changes or risks, and customer is aware of scope."
    gantt_data_suggested.append(['Finish SOW', str(project['Mechanical_Release'] - timedelta(weeks=2)), str(project['Mechanical_Release'] - timedelta(weeks=1))])
    suggested_sched[str(proj_number) + ': ' + 'Order the Robot'] = project['Assembly'] - timedelta(weeks=8), "6-8 Week lead time before the day Assembly starts"
    gantt_data_suggested.append(['Order the Robot', str(project['Assembly'] - timedelta(weeks=8)), str(project['Assembly'] - timedelta(weeks=6))])
    suggested_sched[str(proj_number) + ': ' + 'Manufacturing to Assembly Transition Meeting'] = project['Finishing'] - timedelta(weeks=1), "Allows for 1 week to review items that need to get done for Assembly"
    gantt_data_suggested.append(['Manufacturing/Assembly Transition', str(project['Assembly'] - timedelta(weeks=1)), str(project['Assembly'] - timedelta(days=5))])
    suggested_sched[str(proj_number) + ': ' + 'Assembly to Integration Transition Meeting'] = project['Assembly'] - timedelta(weeks=1), "Allows for 1 week to review items that need to be done for Programmers to start"
    gantt_data_suggested.append(['Assembly/Integration Transition', str(project['Integration'] - timedelta(weeks=1)), str(project['Integration'] - timedelta(days=5))])
    suggested_sched[str(proj_number) + ': ' + 'Prepare for Customer Visit'] = project['Customer_Runoff'] - timedelta(weeks=1), "Customer run off is 1 week after this date"
    gantt_data_suggested.append(['Prepare for Customer Visit', str(project['Customer_Runoff'] - timedelta(days=9)), str(project['Customer_Runoff'] - timedelta(days=5))])
    suggested_sched[str(proj_number) + ': ' + 'Prepare Acieta Run-Off Document'] = project['Customer_Runoff'] - timedelta(days=3), "For the customer to sign for run off at Acieta"
    gantt_data_suggested.append(['Prepare Acieta Run-off Document', str(project['Internal_Runoff'] - timedelta(weeks=1)), str(project['Internal_Runoff'] - timedelta(days=5))])
    suggested_sched[str(proj_number) + ': ' + 'Prepare Shipping Document'] = project['Ship'] - timedelta(weeks=2), "Gives 2 weeks lead time before Ship date"
    gantt_data_suggested.append(['Prepare Shipping Document', str(project['Ship'] - timedelta(days=9)), str(project['Ship'] - timedelta(days=7))])
    suggested_sched[str(proj_number) + ': ' + 'Prepare Final Run-Off Document'] = project['Install_Finish'] - timedelta(weeks=1), "1 week before install finish"
    gantt_data_suggested.append(['Prepare Final Run-Off Document', str(project['Install_Finish'] - timedelta(weeks=1)), str(project['Install_Finish'] - timedelta(days=2))])
    suggested_sched[str(proj_number) + ': ' + 'Prepare T&E Document and Expectations'] = project['Install_Start'] - timedelta(weeks=1), "1 week before install starts"
    gantt_data_suggested.append(['Prepare T&E_Doc/Expectations', str(project['Install_Start'] - timedelta(weeks=1)), str(project['Install_Start'] - timedelta(days=5))])
    suggested_sched[str(proj_number) + ': ' + 'Recieve Approvals on Drawings/SOW from Customer'] = project['Mechanical_Release'] - timedelta(days=5), "Follow up on getting drawings signed, at this point could cause delays to Manufacturing"
    gantt_data_suggested.append(['Recieve Approvals', str(project['Mechanical_Release'] - timedelta(days=7)), str(project['Mechanical_Release'] - timedelta(days=5))])
    suggested_sched[str(proj_number) + ': ' + 'Risk Assessment'] = project['engineering_start'] + timedelta(weeks=2), "2 weeks after engineering starts, risk assessment to determine if design changes need to occur"


    #creating ordered list of dates and descriptions
    list_suggested_schedule = []
    for k, v in suggested_sched.items():
        item = [v[0], v[1], k]
        list_suggested_schedule.append(item)

    print(list_suggested_schedule)
    gantt_data_suggested = sorted(gantt_data_suggested, key=operator.itemgetter(1))
    sorted_list_sugg_sched = sorted(list_suggested_schedule)

    sorted_dict_sugg_sched = dict((z, [x, y]) for x, y, z in sorted_list_sugg_sched)




    print(sorted_dict_sugg_sched)
    return sorted_dict_sugg_sched, gantt_data_suggested

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
