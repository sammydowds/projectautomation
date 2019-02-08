from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from projects.models import *
from projects.forms import *
import datetime

# Create your views here.

#main project page
def index(request):
    #pulling all current projects 
    projects_list = Project.objects.exclude(iscurrent=False)
    print(projects_list)
    context = {
        'projects': projects_list,
    }
    print(projects_list)
    return render(request, "projects/project.html", context)

def update(request, num):
    #if get request, render form with initial values of the project plugged ing
    if request.method == "GET":
        #pulling project number from request
        print("GREAT SUCCESS")
        project_num = num
        print(project_num)
        #pulling project from database
        proj_current = Project.objects.get(projectnumber=project_num)
        print(proj_current)
        form = ProjectForm(initial = proj_current.__dict__)

        return render(request, "projects/update.html", {'form': form, 'project': proj_current})
    #if post request, post updates into the database and return back to the main projects page
    if request.method == "POST":
        print("GREAT SUCCESS 2")

        proj_updating = Project.objects.get(projectnumber = num)
        form = ProjectForm(request.POST, instance=proj_updating)
        if form.is_valid():
            form.save()
        return redirect('/projects')

#creating a project
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
                                  onwatch = True)
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

def switch(request):
    #switching value in database when button is clicked for certain project number
    #saving request data to var for query
    print(request.POST['projectnumber'])
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
    return HttpResponse("Successfully sent request, but did you send data??")

#closing out a project based on a get request - note need to update this method.
def close(request, num):
    if request.method == "GET":
        project_close = num
        print(project_close)
        proj = Project.objects.get(projectnumber=num)
        proj.iscurrent = False
        proj.save()
        return redirect('/projects')


def dashboard(request,num):
    if request.method == "GET":
        project_dash = Project.objects.get(projectnumber=num)
        project_dash = project_dash.__dict__
        print(project_dash)
        milestones = []
        proj_dash = list(project_dash.items())

        for i in range(4, 28):
            print(proj_dash[i])
            if i % 2 == 0 and proj_dash[i+1][1] == False:
                milestones.append(proj_dash[i])
        milestones = dict(milestones)
        date_today = datetime.datetime.today()
        print(date_today)


        #pull project information there
        #plug it into the template, and render it
        return render(request, 'projects/dashboard.html', {'project': project_dash, 'milestones': milestones, 'date_today':date_today})


def milestonescomplete(request):
    if request.method == "POST":
        #saving request data
        projectnumber = request.POST['projectnumber']
        milestone = request.POST['milestone']
        milestone_status = milestone + 'complete'
        print(milestone)

        #query the database for matching project
        project = Project.objects.get(projectnumber=projectnumber)

        #pull current boolean/status of the milestone
        current = getattr(project, milestone_status)

        #updating the milestone status to be the opposite of the current one
        setattr(project, milestone_status, not current)

        project.save()
        return redirect('/projects')
