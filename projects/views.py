
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from projects.models import *
from projects.forms import *
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#TODO create project visualization page - which outputs suggested schedule and visualization of that schedule. Include the critical path of the project if possible. Graph of project - best visualization tool. Try to show critical path, and decisions.
#TODO a calendar flow chart would be amazing. Look into doing this instead of a traditional graph?
#TODO show % breakdown of the project by phase, how many days between each milestone. Sum total business hours per group, as well as days.


@login_required
def index(request):
    user = request.user
    # pulling all current projects
    #
    # -----------------Here is the code to upload all projects from an excel sheet below ------------------------------
    # test_proj = list_projects()
    # for proj in test_proj:
    #     imported_proj = Project(**proj)
    #     imported_proj.save()
    # -----------------------------------------------------------------------------------------------------------------
    projects_list = Project.objects.all().exclude(iscurrent=False)
    print(projects_list)
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    context = {
        'projects': projects_list,
        'num_proj': num_proj,
        'today': date.today(),
        'status': 'Current'
    }
    print(context['projects'])
    return render(request, "projects/main_page.html", context)


@login_required
def pastprojects(request):
    user = request.user
    projects_list = Project.objects.all().exclude(iscurrent=True)
    print(projects_list)
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    context = {
        'projects': projects_list,
        'num_proj': num_proj,
        'today': date.today(),
        'status': 'Past'

    }
    print(context['projects'])
    return render(request, "projects/main_page.html", context)

@login_required
def offtrack(request):
    user = request.user
    projects_list = Project.objects.all().filter(iscurrent=True, Status='offtrack')
    print(projects_list)
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    context = {
        'projects': projects_list,
        'num_proj': num_proj,
        'today': date.today(),
        'status': 'Current'

    }
    print(context['projects'])
    return render(request, "projects/main_page.html", context)

@login_required
def onwatch(request):
    user = request.user
    projects_list = Project.objects.all().filter(iscurrent=True, Status='onwatch')
    print(projects_list)
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    context = {
        'projects': projects_list,
        'num_proj': num_proj,
        'today': date.today(),
        'status': 'Current'

    }
    print(context['projects'])
    return render(request, "projects/main_page.html", context)

@login_required
def projectcards(request):
    user = request.user

    projects_list = Project.objects.all().exclude(iscurrent=False)
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    context = {
        'projects': projects_list,
        'num_proj': num_proj
    }
    return render(request, "projects/main_page.html", context)


# @login_required
# def myprojects(request):
#     user = request.user
#
#     projects_list = Project.objects.filter(projectmanager=request.user).order_by('-lastupdated').exclude(iscurrent=False)
#     # projects_list = reversed(projects_list.exclude(iscurrent=False))
#     num_proj = projects_list.count()
#     projects_on_watch = Project.objects.filter(projectmanager=request.user).exclude(onwatch=False)
#     projects_off_track = Project.objects.filter(projectmanager=request.user).exclude(offtrack=False)
#
#     context = {
#         'projects': projects_list,
#         'num_proj': num_proj,
#         'projects_watch': projects_on_watch,
#         'projects_off': projects_off_track
#     }
#     return render(request, "projects/myprojects.html", context)


#page for updating a project
@login_required
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
        return redirect('/projects/')


#creating a project

@login_required
def create(request):
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
                                  Status = form.cleaned_data["Status"], \
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

#handles AJAX request to switch a project from on watch to off, or on track to off
@login_required
def switch(request):
    #switching value in database when button is clicked for certain project number
    #saving request data to var for query
    projectnumber = request.POST['projectnumber']
    type = request.POST['type']

    #query the database for matching project
    project = Project.objects.get(projectnumber=projectnumber)

    #switching value
    if type == "onwatch":
        project.onwatch = not project.onwatch
    else:
        project.offtrack = not project.offtrack

    #submitting switched values to the database
    project.save()

    #switch value base on current value
    return redirect("/projects/")

#closing out a project based on a get request - note need to update this method.
@login_required
def activation(request, num):
    if request.method == "GET":
        project_close = num
        proj = Project.objects.get(projectnumber=num)
        proj.iscurrent = not proj.iscurrent
        proj.save()
        return redirect('/projects')


#handles AJAX request to mark a milestone complete in the database
@login_required
def milestonescomplete(request):
    if request.method == "POST":
        #saving request data
        projectnumber = request.POST['projectnumber']
        milestone = request.POST['milestone']
        milestone_status = milestone + 'complete'

        #query the database for matching project
        project = Project.objects.get(projectnumber=projectnumber)

        #pull current boolean/status of the milestone
        current = getattr(project, milestone_status)

        #updating the milestone status to be the opposite of the current one
        setattr(project, milestone_status, not current)

        project.save()
        return redirect('/projects')

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
