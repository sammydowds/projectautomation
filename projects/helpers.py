from datetime import *
from django.db import models
from dateutil.relativedelta import relativedelta
from projects.models import *
import json
import operator
from calendar import *

#combines all projects by phase and includes a list of dictionaries
def all_phases():
    #pulling all projects from the DB that are current
    projects = Project.objects.exclude(iscurrent=False)
    #Empty dict for storing the phases of all relevant phases of projects
    project_phases = {}
    #looping through list of projects in DB
    for project in projects:
        #getting phases of this project
        this_project_phases = project.phases()
        #iterating over phases of this project
        for key, value in this_project_phases.items():
            start = value['start']
            end = value['end']
            this_year = datetime.now()
            this_year = this_year.year
            #checking to make sure all dates are entered, and the end date is after today (to ensure relevant graph)
            if start != None and end != None and value['duration'] >= 0:
                if key in project_phases:
                    project_phases[key].append({'number': project.projectnumber, 'name': project.projectname, 'dates': value})
                else:
                    project_phases[key] =[]
                    project_phases[key].append({'number': project.projectnumber, 'name': project.projectname, 'dates': value})

    return project_phases


def capacity_by_month(phases = all_phases()):
    if phases:
        del phases['Project']
    monthly_capacity = {}
    for phase, info in phases.items():

        for project in info:
            start = project['dates']['start']
            end = project['dates']['end']
            start_month = month_abbr[start.month]
            end_month = month_abbr[end.month]

            #checking to make sure the phase is a key in our dict.
            if phase not in monthly_capacity.keys():
                monthly_capacity[phase]=months_to_year(start.year)
                monthly_capacity[phase]=months_to_year(end.year)

            # checking if year is in dict, if not add element
            if start.year not in monthly_capacity[phase]:
                monthly_capacity[phase].update(months_to_year(start.year))
            elif end.year not in monthly_capacity[phase]:
                monthly_capacity[phase].update(months_to_year(end.year))

            #checking how many months are between end and start
            delta = relativedelta(end, start)

            #checking to see if there is a month(s) in between start and end dates
            if delta.months >=2:
                month_from_start = start
                for month in range(0, delta.months+1):
                    date_m = month_from_start + relativedelta(months=+month)
                    date_months = month_abbr[date_m.month]
                    monthly_capacity[phase][date_m.year][date_months] = monthly_capacity[phase][date_m.year][date_months] + 1
            #if there is 1 month or less between dates
            else:
                monthly_capacity[phase][start.year][start_month] = monthly_capacity[phase][start.year][start_month] + 1
                if start.month != end.month and delta.months <= 1:
                    monthly_capacity[phase][end.year][end_month] = monthly_capacity[phase][end.year][end_month] + 1


    return monthly_capacity

def months_to_year(year):
    months = {'Jan': 0, 'Feb': 0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0}
    return {year: months}

#parsing data for area gantt chart and forecasting capcity needs
def google_area_chart(data = capacity_by_month(), years_ahead = 1):
    #setting up list for columns [months, phases 1, phase 2,...phase n]
    columns = [('string', 'months'),]

    #creating array of years ahead based on how many years you want to look ahead
    this_year = datetime.now()
    this_year = this_year.year
    years = []
    chart_data = {}

    #appending years, and structuring chart data
    for i in range(0, years_ahead+1):
        years.append(this_year + i)
        chart_data[this_year+i] = [['Jan'], ['Feb'],['Mar'],['Apr'],['May'],['Jun'],['Jul'],['Aug'],['Sep'],['Oct'],['Nov'],['Dec']]

    #iterating through each phase (key = phase)
    for key in data.keys():
        #appending the phase to the columns list
        phase = key
        columns.append(('number', phase))
        #looping through the years

    #looping through phases
    for year, row in chart_data.items():
        #for element in row to append to
        for element in row:
            month = element[0]
            for phase, years_data in data.items():
                if year in years_data:
                    months = data[phase][year]
                    if month in months:
                        element.append(months[month])
                    else:
                        element.append(0)

                else:
                    element.append(0)
        chart_data[year]= ([columns] + row)
    print(chart_data)
    return columns, chart_data
