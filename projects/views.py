
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

    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    #number of project off track
    num_off = projects_list.filter(Status="offtrack").count()
    #number of project on watch
    num_watch = projects_list.filter(Status="onwatch").count()
    #number of project on track
    num_on = projects_list.filter(Status="ontrack").count()
    #saving info to pass to the template
    is_pm = request.user.groups.filter(name='Project_Manager').exists()
    context = {
        'projects': projects_list,
        'num_proj': num_proj,
        'today': date.today(),
        'num_off': num_off,
        'num_watch': num_watch,
        'num_on': num_on,
        'status': 'Current',
        'is_pm': is_pm,
        'Title': 'All Projects'
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
    is_pm = request.user.groups.filter(name='Project_Manager').exists()
    context = {
        'count': len(projects_list),
        'projects': projects_list,
        'today': date.today(),
        'status': 'Current',
        'is_pm': is_pm
    }
    return render(request, "projects/base_myprojects.html", context)

#printable version of projects
@login_required
@never_cache
def printable(request):
    #TODO: condense all HTML views to run through this one
    user = request.user
    filtered_projects = []
    projects = Project.objects.all().order_by('projectnumber').filter(iscurrent=True)
    now = datetime.datetime.now()
    context = {
        'projects': projects,
        'time': now,
        'title': 'All Projects'
    }
    return render(request, "projects/base_printprojects.html", context)

#printable version of projects
@login_required
@never_cache
def myprintable(request):
    #TODO: condense all HTML views to run through this one
    user = request.user
    filtered_projects = []
    projects = Project.objects.filter(projectmanager=user)
    now = datetime.datetime.now()
    context = {
        'projects': projects,
        'time': now,
        'title': str(user.first_name) + "'s Projects"
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
    is_pm = request.user.groups.filter(name='Project_Manager').exists()
    context = {
        'title': 'Past',
        'projects': projects_list,
        'num_proj': num_proj,
        'today': date.today,
        'status': 'Past',
        'is_pm': is_pm
    }
    return render(request, "projects/base_projects.html", context)

#breaking down projects by milestones and deadlines
@login_required
@never_cache
def planner(request):
    projects = Project.objects.all().order_by('projectnumber').exclude(iscurrent=False, )
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    context = {
        'projects': projects,
        'today': datetime.datetime.now(),
        'list_milestones': ['MilestoneOne',\
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
                                  MilestoneOne = form.cleaned_data["MilestoneOne"],\
                                  MilestoneTwo = form.cleaned_data["MilestoneTwo"],\
                                  MilestoneThree = form.cleaned_data["MilestoneThree"],\
                                  MilestoneFour = form.cleaned_data["MilestoneFour"],\
                                  MilestoneFive = form.cleaned_data["MilestoneFive"],\
                                  MilestoneSix = form.cleaned_data["MilestoneSix"],\
                                  MilestoneSeven = form.cleaned_data["MilestoneSeven"],\
                                  Status="onwatch",\
                                  projectmanager=form.cleaned_data["projectmanager"] )
            #adding the new project to the initial project table
            #note: there has to be a better way to convert a form directly to an object below....!
            initial_project = InitialProject(projectname = form.cleaned_data["projectname"],
                                  projectnumber = form.cleaned_data["projectnumber"],\
                                  MilestoneOne = form.cleaned_data["MilestoneOne"],\
                                  MilestoneTwo = form.cleaned_data["MilestoneTwo"],\
                                  MilestoneThree = form.cleaned_data["MilestoneThree"],\
                                  MilestoneFour = form.cleaned_data["MilestoneFour"],\
                                  MilestoneFive = form.cleaned_data["MilestoneFive"],\
                                  MilestoneSix = form.cleaned_data["MilestoneSix"],\
                                  MilestoneSeven = form.cleaned_data["MilestoneSeven"],\
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
#returns projects ontrack
@login_required
@never_cache
def viewontrack(request):
    #TODO: condense all HTML views to run through this one
    user = request.user

    projects_list= Project.objects.all().exclude(iscurrent=False)
    projects_list_ontrack = Project.objects.all().exclude(iscurrent=False).filter(Status='ontrack')
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    #number of project off track
    num_off = projects_list.filter(Status="offtrack").count()
    #number of project on watch
    num_watch = projects_list.filter(Status="onwatch").count()
    #number of project on track
    num_on = projects_list.filter(Status="ontrack").count()
    #saving info to pass to the template
    is_pm = request.user.groups.filter(name='Project_Manager').exists()
    context = {
        'projects': projects_list_ontrack,
        'num_proj': num_proj,
        'today': date.today(),
        'num_off': num_off,
        'num_watch': num_watch,
        'num_on': num_on,
        'status': 'Current',
        'is_pm': is_pm,
        'Title': 'On Track'
    }
    return render(request, "projects/base_projects.html", context)

#returns projects ontrack
@login_required
@never_cache
def viewofftrack(request):
    #TODO: condense all HTML views to run through this one
    user = request.user
    projects_list= Project.objects.all().exclude(iscurrent=False)
    projects_list_off = Project.objects.all().exclude(iscurrent=False).filter(Status='offtrack')
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    #number of project off track
    num_off = projects_list.filter(Status="offtrack").count()
    #number of project on watch
    num_watch = projects_list.filter(Status="onwatch").count()
    #number of project on track
    num_on = projects_list.filter(Status="ontrack").count()
    #saving info to pass to the template
    is_pm = request.user.groups.filter(name='Project_Manager').exists()
    context = {
        'projects': projects_list_off,
        'num_proj': num_proj,
        'today': date.today(),
        'num_off': num_off,
        'num_watch': num_watch,
        'num_on': num_on,
        'status': 'Current',
        'is_pm': is_pm,
        'Title': 'Off Track'
    }
    return render(request, "projects/base_projects.html", context)

#returns projects ontrack
@login_required
@never_cache
def viewonwatch(request):
    #TODO: condense all HTML views to run through this one
    user = request.user

    projects_list= Project.objects.all().exclude(iscurrent=False)
    projects_list_onwatch = Project.objects.all().exclude(iscurrent=False).filter(Status='onwatch')
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    #number of project off track
    num_off = projects_list.filter(Status="offtrack").count()
    #number of project on watch
    num_watch = projects_list.filter(Status="onwatch").count()
    #number of project on track
    num_on = projects_list.filter(Status="ontrack").count()
    #saving info to pass to the template
    is_pm = request.user.groups.filter(name='Project_Manager').exists()
    context = {
        'projects': projects_list_onwatch,
        'num_proj': num_proj,
        'today': date.today(),
        'num_off': num_off,
        'num_watch': num_watch,
        'num_on': num_on,
        'status': 'Current',
        'is_pm': is_pm,
        'Title': 'On Watch'
    }
    return render(request, "projects/base_projects.html", context)


#closing out a project based on a get request - note need to update this method.
@login_required
@never_cache
#TODO changing state on GET request - look at??
def activation(request, num):
    if request.method == "GET":
        project_close = num
        proj = Project.objects.get(projectnumber=num)
        proj.iscurrent = not proj.iscurrent
        proj.save()
        return redirect('/projects')

#TODO: note, this is probably bad design to have two schedule functions for marking True and False - might consider switching to one
#marking scheduled as true
@login_required
@never_cache
def scheduled(request):
    if request.method == "POST":
        num = request.POST['projectnumber']
        milestone = request.POST['milestone']
        proj = Project.objects.get(projectnumber=num)
        if milestone == 'Install_Start_Scheduled':
            setattr(proj, 'Install_Finish_Scheduled', True)
        if milestone == 'Manufacturing_Scheduled':
            setattr(proj, 'Finishing_Scheduled', True)
        setattr(proj, milestone, True)
        proj.save()
        return redirect('/projects/planner')
    else:
        return redirect('/projects/')

#marking scheduled as false
@login_required
@never_cache
def notscheduled(request):
    if request.method == "POST":
        num = request.POST['projectnumber']
        milestone = request.POST['milestone']
        proj = Project.objects.get(projectnumber=num)
        if milestone == 'Install_Start_Scheduled':
            setattr(proj, 'Install_Finish_Scheduled', False)
        if milestone == 'Manufacturing_Scheduled':
            setattr(proj, 'Finishing_Scheduled', False)
        setattr(proj, milestone, False)
        proj.save()
        return redirect('/projects/planner')
    else:
        return redirect('/projects/')

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
