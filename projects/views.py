
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
    #     saving_initial = InitialProject(**proj)
    #     imported_proj.save()
    #     saving_initial.save()
    projects_list = Project.objects.all().exclude(iscurrent=False).order_by('projectnumber')
    #code below is to convert all project into intial project models
    # for project in projects_list:
    #     form = project.__dict__
    #     initial_project = InitialProject(projectname = form["projectname"],
    #                           projectnumber = form["projectnumber"],\
    #                           Mechanical_Release = form["Mechanical_Release"],\
    #                           Electrical_Release = form["Electrical_Release"],\
    #                           Manufacturing = form["Manufacturing"],\
    #                           Finishing = form["Finishing"],\
    #                           Assembly = form["Assembly"],\
    #                           Internal_Runoff = form["Internal_Runoff"],\
    #                           Customer_Runoff = form["Customer_Runoff"],\
    #                           Ship = form["Ship"],\
    #                           Install_Start = form["Install_Start"],\
    #                           Install_Finish = form["Install_Finish"],\
    #                           Documentation = form["Documentation"], \
    #                           Status = 'onwatch', \
    #                           )
    #     initial_project.save()

    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    #number of project off track
    num_off = projects_list.filter(Status="offtrack").count()
    #number of project on watch
    num_watch = projects_list.filter(Status="onwatch").count()
    #number of project on track
    num_on = projects_list.filter(Status="ontrack").count()
    #saving info to pass to the template
    context = {
        'projects': projects_list,
        'num_proj': num_proj,
        'today': date.today(),
        'num_off': num_off,
        'num_watch': num_watch,
        'num_on': num_on,
        'status': 'Current'
    }
    return render(request, "projects/base_projects.html", context)

@login_required
@never_cache
def thisweek(request):
    user = request.user

    #list of current projects
    projects = Project.objects.all().filter(iscurrent=True)

    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    context = {
        'projects': projects,
        'today': date.today(),
    }
    return render(request, "projects/base_week.html", context)

#project manager dashboard
@login_required
@never_cache
def myprojects(request):
    user = request.user
    #pulling all active projects
    projects_list = Project.objects.all().exclude(iscurrent=False).filter(projectmanager=user).order_by('projectnumber')

    context = {
        'count': len(projects_list),
        'projects': projects_list,
        'today': date.today(),
        'status': 'Current'
    }
    return render(request, "projects/base_myprojects.html", context)

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
    return render(request, "projects/base_printprojects.html", context)

#past projects main page
@login_required
@never_cache
def pastprojects(request):
    user = request.user
    projects_list = Project.objects.all().exclude(iscurrent=True)
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    context = {
        'title': 'Past',
        'projects': projects_list,
        'num_proj': num_proj,
        'today': date.today(),
        'status': 'Past'
    }
    return render(request, "projects/base_projects.html", context)

#breaking down projects by milestones and deadlines
@login_required
@never_cache
def planner(request):
    user = request.user
    today = datetime.datetime.now()
    #note, probably better way to do the following
    parsed_milestones = []
    parsed_milestones.append({'Mechanical Engineering': list(Project.objects.all().filter(iscurrent=True, Mechanical_Release__gte=today).order_by('Mechanical_Release').values('projectnumber','projectname','Mechanical_Release', 'Status', 'lastupdated'))})
    parsed_milestones.append({'Electrical Engineering': list(Project.objects.all().filter(iscurrent=True, Electrical_Release__gte=today).order_by('Electrical_Release').values('projectnumber','projectname','Electrical_Release', 'Status', 'lastupdated'))})
    parsed_milestones.append({'Manufacturing': list(Project.objects.all().filter(iscurrent=True, Manufacturing__gte=today).order_by('Manufacturing').values('projectnumber','projectname','Manufacturing', 'Status', 'lastupdated'))})
    parsed_milestones.append({'Finishing': list(Project.objects.all().filter(iscurrent=True, Finishing__gte=today).order_by('Finishing').values('projectnumber','projectname','Finishing', 'Status', 'lastupdated'))})
    parsed_milestones.append({'Assembly': list(Project.objects.all().filter(iscurrent=True, Assembly__gte=today).order_by('Assembly').values('projectnumber','projectname','Assembly', 'Status', 'lastupdated'))})
    parsed_milestones.append({'Ship': list(Project.objects.all().filter(iscurrent=True, Ship__gte=today).order_by('Ship').values('projectnumber','projectname','Ship', 'Status', 'lastupdated'))})
    parsed_milestones.append({'Integration': list(Project.objects.all().filter(iscurrent=True, Customer_Runoff__gte=today).order_by('Customer_Runoff').values('projectnumber','projectname', 'Internal_Runoff', 'Customer_Runoff', 'Status', 'lastupdated'))})

    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    context = {
        'info': parsed_milestones,
        'time': datetime.datetime.now(),
        'status': 'Past'

    }
    return render(request, "projects/base_planner.html", context)

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
        #setting form initial to project current dict
        form = ProjectForm(initial = proj_current.__dict__)

        return render(request, "projects/update.html", {'form': form, 'project': proj_current, 'today': datetime.date.today()})

    #if post request, post updates into the database and return back to the main projects page
    if request.method == "POST":
        proj_updating = Project.objects.get(projectnumber = num)
        proj_updating.lastupdated = date.today()
        proj_updating.save()
        form = ProjectForm(request.POST, instance=proj_updating)

        if form.is_valid():
            form.save()

        #updating the slippage of the current milestone
        if InitialProject.objects.get(projectnumber=num):
            #saving current project
            proj = Project.objects.get(projectnumber=num)
            #looking up the initial project
            init_proj = InitialProject.objects.get(projectnumber=num)
            #saving current milestone
            milestone = proj.current_milestone()
            #converting init_proj to dict to look up current milestone
            init_proj = init_proj.__dict__
            #calculating timedelta

            if milestone['name'] != 'Review Dates' and init_proj[milestone['name']] != None:
                slippage = milestone['end']-init_proj[milestone['name']]
                proj.Slippage = int((slippage.days)/7)
            else:
                proj.Slippage = proj.Slippage

            #saving project slippage to the model
            proj.save()


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

@login_required
def milestonecomplete(request):
    if request.method == "POST":
        #saving request data
        print("Test")
        projectnumber = request.POST['projectnumber']
        milestone = request.POST['milestone']
        milestone_status = milestone + '_Complete'
        print(milestone_status)

        #query the database for matching project
        project = Project.objects.get(projectnumber=projectnumber)
        print(project)

        #pull current boolean/status of the milestone
        current = getattr(project, milestone_status)

        #updating the milestone status to be the opposite of the current one
        setattr(project, milestone_status, not current)
        project.save()

        #updating project slippage (because new current milestone has changed) - note this is repeat code, should combine it into one function
        #updating the slippage of the current milestone
        if InitialProject.objects.get(projectnumber=projectnumber):
            #saving current project
            proj = Project.objects.get(projectnumber=projectnumber)
            #looking up the initial project
            init_proj = InitialProject.objects.get(projectnumber=projectnumber)
            #saving current milestone
            milestone = proj.current_milestone()
            #converting init_proj to dict to look up current milestone
            init_proj = init_proj.__dict__
            #calculating timedelta

            if milestone['name'] != 'Review Dates' and init_proj[milestone['name']] != None:
                slippage = milestone['end']-init_proj[milestone['name']]
                proj.Slippage = int((slippage.days)/7)
            else:
                proj.Slippage = proj.Slippage

            #saving project slippage to the model
            proj.save()

        return redirect('/projects')

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
