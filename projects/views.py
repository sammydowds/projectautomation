
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from projects.models import *
from projects.forms import *
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from import_projects import import_all_projects
import numpy as np

#main page
@login_required
@never_cache
def index(request):
    #TODO: condense all HTML views to run through this one
    user = request.user
    # pulling all current projects
    #
    # -----------------Here is the code to upload all projects from an excel sheet below ------------------------------
    # test_proj = import_all_projects()
    # for proj in test_proj:
    #     imported_proj = Project(**proj)
    #     imported_proj.save()
    projects_list = Project.objects.all().exclude(iscurrent=False).order_by('projectnumber')

    #TODO update for analyzing slippage
    initial_projects = InitialProject.objects.all()
    slippage = []

    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    num_off = projects_list.filter(Status="offtrack").count()
    num_watch = projects_list.filter(Status="onwatch").count()
    num_on = projects_list.filter(Status="ontrack").count()
    context = {
        'initial_projects': initial_projects,
        'projects': projects_list,
        'num_proj': num_proj,
        'today': date.today(),
        'num_off': num_off,
        'num_watch': num_watch,
        'num_on': num_on,
        'status': 'Current'
    }
    return render(request, "projects/main_page.html", context)

@login_required
@never_cache
def thisweek(request):
    user = request.user
    #saving current week number, if it is saturday or sunday we select it as the next week
    if date.today().isocalendar()[2] >=6:
        week_number = date.today().isocalendar()[1] + 1
    else:
        week_number = date.today().isocalendar()[1]
    #pulling all active projects
    projects_list = Project.objects.all().exclude(iscurrent=False).order_by('projectnumber')
    #empty array to save projects which have a milestone this week
    projects_list_week = []
    #looping through project list
    for project in projects_list:
        if isinstance(project.current_milestone()['end'], datetime.date) == True and (project.current_milestone()['end'].isocalendar()[1]) == week_number:
            var = project.current_milestone()['end']
            projects_list_week.append(project)
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    context = {
        'projects': projects_list_week,
        'today': date.today(),
    }
    print(projects_list_week)
    return render(request, "projects/this_week.html", context)

#project manager dashboard
@login_required
@never_cache
def myprojects(request):
    user = request.user
    #saving current week number
    if date.today().isocalendar()[2] >=6:
        week_number = date.today().isocalendar()[1] + 1
    else:
        week_number = date.today().isocalendar()[1]
    #pulling all active projects
    projects_list = Project.objects.all().exclude(iscurrent=False).filter(projectmanager=user).order_by('projectnumber')
    #empty array to save projects which have a milestone this week
    projects_list_week = []
    #looping through project list
    for project in projects_list:
        if isinstance(project.current_milestone()['end'], datetime.date) == True and (project.current_milestone()['end'].isocalendar()[1]) == week_number:
            var = project.current_milestone()['end']
            projects_list_week.append(project)

    context = {
        'projects': projects_list,
        'projects_this_week': projects_list_week,
        'today': date.today(),
        'status': 'Current'
    }
    return render(request, "projects/main_page_my_projects.html", context)

#printable version of projects
@login_required
@never_cache
def printable(request):
    #TODO: condense all HTML views to run through this one
    user = request.user
    filtered_projects = []
    filtered_projects.append({'Off Track': Project.objects.all().filter(iscurrent=True, Status='offtrack').order_by('-projectnumber')})
    filtered_projects.append({'On Watch': Project.objects.all().filter(iscurrent=True, Status='onwatch').order_by('-projectnumber')})
    filtered_projects.append({'On Track': Project.objects.all().filter(iscurrent=True, Status='ontrack').order_by('-projectnumber')})
    now = datetime.datetime.now()
    context = {
        'filtered_projects': filtered_projects,
        'time': now,
    }
    return render(request, "projects/printable.html", context)

#past projects main page
@login_required
@never_cache
def pastprojects(request):
    user = request.user
    projects_list = Project.objects.all().exclude(iscurrent=True)
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    context = {
        'projects': projects_list,
        'num_proj': num_proj,
        'today': date.today(),
        'status': 'Past'
    }
    return render(request, "projects/main_page.html", context)

#breaking down projects by milestones and deadlines
@login_required
@never_cache
def planner(request):
    user = request.user
    today = datetime.datetime.now()
    #note, probably better way to do the following
    parsed_milestones = []
    parsed_milestones.append({'Mechanical Engineering': list(Project.objects.all().filter(iscurrent=True, Mechanical_Release__gte=today).order_by('Mechanical_Release').values('projectnumber','projectname','Mechanical_Release', 'Status'))})
    parsed_milestones.append({'Electrical Engineering': list(Project.objects.all().filter(iscurrent=True, Electrical_Release__gte=today).order_by('Electrical_Release').values('projectnumber','projectname','Electrical_Release', 'Status'))})
    parsed_milestones.append({'Manufacturing': list(Project.objects.all().filter(iscurrent=True, Manufacturing__gte=today).order_by('Manufacturing').values('projectnumber','projectname','Manufacturing', 'Status'))})
    parsed_milestones.append({'Finishing': list(Project.objects.all().filter(iscurrent=True, Finishing__gte=today).order_by('Finishing').values('projectnumber','projectname','Finishing', 'Status'))})
    parsed_milestones.append({'Assembly': list(Project.objects.all().filter(iscurrent=True, Assembly__gte=today).order_by('Assembly').values('projectnumber','projectname','Assembly', 'Status'))})
    parsed_milestones.append({'Ship': list(Project.objects.all().filter(iscurrent=True, Ship__gte=today).order_by('Ship').values('projectnumber','projectname','Ship', 'Status'))})
    parsed_milestones.append({'Integration': list(Project.objects.all().filter(iscurrent=True, Customer_Runoff__gte=today).order_by('Customer_Runoff').values('projectnumber','projectname', 'Internal_Runoff', 'Customer_Runoff', 'Status'))})

    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    context = {
        'info': parsed_milestones,
        'time': datetime.datetime.now(),
        'status': 'Past'

    }
    return render(request, "projects/main_page_by_milestone.html", context)

#page for updating a project
@login_required
@never_cache
def update(request, num):
    #if get request, render form with initial values of the project plugged ing
    if request.method == "GET":
        #pulling project number from request
        project_num = num
        #pulling project from database
        proj_current = Project.objects.get(projectnumber=project_num)
        form = ProjectForm(initial = proj_current.__dict__)
        return render(request, "projects/update.html", {'form': form, 'project': proj_current})
    #if post request, post updates into the database and return back to the main projects page
    if request.method == "POST":
        proj_updating = Project.objects.get(projectnumber = num)
        proj_updating.lastupdated = date.today()
        proj_updating.save()
        form = ProjectForm(request.POST, instance=proj_updating)

        if form.is_valid():
            form.save()
        return redirect('/projects')


#creating a project
@login_required
@never_cache
def create(request):
    #TODO do not allow duplicate project numbers to be entered
    #Processing POST method (form to create a project)
    if request.method == "POST":
        #need to add filter to ensure project does not already exist with the same projec number
        form = ProjectForm(request.POST)
        if form.is_valid():
            #note: there has to be a better way to convert a form directly to an object below....!
            new_project = Project(projectname = form.cleaned_data["projectname"],
                                  projectnumber = form.cleaned_data["projectnumber"],\
                                  Mechanical_Release = form.cleaned_data["Mechanical_Release"],\
                                  Electrical_Release = form.cleaned_data["Electrical_Release"],\
                                  Manufacturing = form.cleaned_data["Manufacturing"],\
                                  Finishing = form.cleaned_data["Finishing"],\
                                  Assembly = form.cleaned_data["Assembly"],\
                                  Integration = form.cleaned_data["Integration"],\
                                  Internal_Runoff = form.cleaned_data["Internal_Runoff"],\
                                  Customer_Runoff = form.cleaned_data["Customer_Runoff"],\
                                  Ship = form.cleaned_data["Ship"],\
                                  Install_Start = form.cleaned_data["Install_Start"],\
                                  Install_Finish = form.cleaned_data["Install_Finish"],\
                                  Documentation = form.cleaned_data["Documentation"], \
                                  Status="onwatch",\
                                  projectmanager=form.cleaned_data["projectmanager"] )
            #adding the new project to the initial project table
            #note: there has to be a better way to convert a form directly to an object below....!
            initial_project = InitialProject(projectname = form.cleaned_data["projectname"],
                                  projectnumber = form.cleaned_data["projectnumber"],\
                                  Mechanical_Release = form.cleaned_data["Mechanical_Release"],\
                                  Electrical_Release = form.cleaned_data["Electrical_Release"],\
                                  Manufacturing = form.cleaned_data["Manufacturing"],\
                                  Finishing = form.cleaned_data["Finishing"],\
                                  Assembly = form.cleaned_data["Assembly"],\
                                  Integration = form.cleaned_data["Integration"],\
                                  Internal_Runoff = form.cleaned_data["Internal_Runoff"],\
                                  Customer_Runoff = form.cleaned_data["Customer_Runoff"],\
                                  Ship = form.cleaned_data["Ship"],\
                                  Install_Start = form.cleaned_data["Install_Start"],\
                                  Install_Finish = form.cleaned_data["Install_Finish"],\
                                  Documentation = form.cleaned_data["Documentation"], \
                                  Status = 'onwatch', \
                                  )

            #adding the new project to the database
            new_project.save()
            initial_project.save()
            return redirect('/projects/')
    elif request.method == "GET":
        #presenting empty form to the client
        form = ProjectForm()
        return render(request, "projects/create.html", {'form': form})

#view for people not logged in to see status of project
def projectstatus(request, num):
    if request.method == "GET":
        proj = Project.objects.get(projectnumber=num)
        context = {
            'project': proj
            }
        return render(request, 'projects/projectstatus.html', context)

#deleting a project from the db
@login_required
@never_cache
def delete(request, num):
    if request.method == "GET":
        proj = Project.objects.get(projectnumber=num)
        proj.delete()
        return redirect('/projects/pastprojects')

#updating project ontrack
@login_required
@never_cache
def ontrack(request):
    if request.method == "POST":
        num = request.POST['projectnumber']
        proj = Project.objects.get(projectnumber=num)
        proj.Status = "ontrack"
        proj.save()
    else:
        return redirect('/projects/')
#updating project offtrack
@login_required
@never_cache
def offtrack(request):
    if request.method == "POST":
        num = request.POST['projectnumber']
        proj = Project.objects.get(projectnumber=num)
        proj.Status = "offtrack"
        proj.save()
    else:
        return redirect('/projects/')
#updating project onwatch
@login_required
@never_cache
def onwatch(request):
    if request.method == "POST":
        num = request.POST['projectnumber']
        proj = Project.objects.get(projectnumber=num)
        proj.Status = "onwatch"
        proj.save()
    else:
        return redirect('/projects/')

#closing out a project based on a get request - note need to update this method.
@login_required
@never_cache
def activation(request, num):
    if request.method == "GET":
        project_close = num
        proj = Project.objects.get(projectnumber=num)
        proj.iscurrent = not proj.iscurrent
        proj.save()
        return redirect('/projects')

#logout user
def logout(request):
    logout(request)
    return redirect('/projects')

#TODO need to add where if the username already exists in the system it throws an error
def register(request):
    if request.method == 'GET':
        form = RegisterExtendedForm()
        return render(request, 'registration/register.html', {'form': form})
    if request.method == 'POST':
        form = RegisterExtendedForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password1'],
                                         first_name=form.cleaned_data['first_name'],
                                         last_name=form.cleaned_data['last_name'])

            user.save()
            return redirect('/projects')


# In memory: Stretchy - my stepfather. Lost him March 20th, 2019 during this project.
