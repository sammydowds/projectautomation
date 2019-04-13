from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from projects.models import *
from projects.forms import *
import datetime
from projects.helpers import *
from projects.import_proj import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
    # # -----------------------------------------------------------------------------------------------------------------
    projects_list = Project.objects.all()
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    context = {
        'projects': projects_list,
        'num_proj': num_proj
    }
    return render(request, "projects/project.html", context)

@login_required
def myprojects(request):
    user = request.user
    # pulling all current projects
    #
    # -----------------Here is the code to upload all projects from an excel sheet below ------------------------------
    # test_proj = list_projects()
    # for proj in test_proj:
    #     imported_proj = Project(**proj)
    #     imported_proj.save()
    # # -----------------------------------------------------------------------------------------------------------------
    projects_list = Project.objects.filter(projectmanager=request.user)
    # projects_list = reversed(projects_list.exclude(iscurrent=False))
    num_proj = projects_list.count()
    context = {
        'projects': projects_list,
        'num_proj': num_proj
    }
    return render(request, "projects/myprojects.html", context)


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
        form = ProjectForm(request.POST, instance=proj_updating)

        if form.is_valid():
            form.save()
        return redirect('/projects')


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
                                  mechanicalrelease = form.cleaned_data["mechanicalrelease"],\
                                  electricalrelease = form.cleaned_data["electricalrelease"],\
                                  manufacturing = form.cleaned_data["manufacturing"],\
                                  finishing = form.cleaned_data["finishing"],\
                                  assembly = form.cleaned_data["assembly"],\
                                  integration = form.cleaned_data["integration"],\
                                  internalrunoff = form.cleaned_data["internalrunoff"],\
                                  customerrunoff = form.cleaned_data["customerrunoff"],\
                                  ship = form.cleaned_data["ship"],\
                                  installstart = form.cleaned_data["installstart"],\
                                  installfinish = form.cleaned_data["installfinish"],\
                                  documentation = form.cleaned_data["documentation"], \
                                  offtrack = True, \
                                  onwatch = True, \
                                  projectmanager=form.cleaned_data["projectmanager"] )
            #adding the new project to the initial project table
            #note: there has to be a better way to convert a form directly to an object below....!
            initial_project = InitialProject(projectname = form.cleaned_data["projectname"],
                                  projectnumber = form.cleaned_data["projectnumber"],\
                                  mechanicalrelease = form.cleaned_data["mechanicalrelease"],\
                                  electricalrelease = form.cleaned_data["electricalrelease"],\
                                  manufacturing = form.cleaned_data["manufacturing"],\
                                  finishing = form.cleaned_data["finishing"],\
                                  assembly = form.cleaned_data["assembly"],\
                                  integration = form.cleaned_data["integration"],\
                                  internalrunoff = form.cleaned_data["internalrunoff"],\
                                  customerrunoff = form.cleaned_data["customerrunoff"],\
                                  ship = form.cleaned_data["ship"],\
                                  installstart = form.cleaned_data["installstart"],\
                                  installfinish = form.cleaned_data["installfinish"],\
                                  documentation = form.cleaned_data["documentation"], \
                                  offtrack = True, \
                                  onwatch = True)
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
def close(request, num):
    if request.method == "GET":
        project_close = num
        proj = Project.objects.get(projectnumber=num)
        proj.iscurrent = False
        proj.save()
        return redirect('/projects')

#passes project data, milestones abstracted, today's date and the phase which the project is in to the HTML template
@login_required
def dashboard(request,num):
    if request.method == "GET":
        #pulling information from database for the project number
        proj = Project.objects.get(projectnumber=num)
        #plug it into the template, and render it
        return render(request, 'projects/dashboard.html', {'project': proj, 'milestones': proj.milestones_remaining(), 'date_today': date.today(), 'phase': proj.current_phase()})

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

#returns dictionary of dates related to each department
@login_required
def capacity(request):
    if request.method == "GET":
        capacity_company, capacity_an = capacity_analysis()
        return render(request, 'projects/capacity.html', {"capacity": capacity_company, "capacity_analysis": capacity_an})

#renders suggested schedule based on suggest_schedule algorithm
@login_required
def suggested(request, num):
    if request.method == "GET":
        project=Project.objects.get(projectnumber=num)
        suggested_schedule_an = suggest_schedule(project)
        project_details = {"project_num": project.projectnumber, "project_name": project.projectname}

        return render(request, 'projects/suggested.html', {'suggested_schedule_analysis': suggested_schedule_an, "projectdetails": project_details })

#renders suggested schedule based on suggest_schedule algorithm  for each of the projects in the database
@login_required
def tasks(request):
    if request.method == "GET":
        projects = Project.objects.filter(projectmanager=request.user.username, iscurrent=True)
        project_tasks = []
        for project in projects:
            project_tasks.append(suggest_schedule(project))
        ordered_tasks = organize_tasks(project_tasks)
        return render(request, 'projects/tasks.html', {'sorted_tasks': ordered_tasks, 'number_tasks': len(ordered_tasks)})

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
