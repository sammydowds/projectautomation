from django.shortcuts import render, redirect
from django.http import HttpResponse
from projects.models import *
from projects.forms import *

# Create your views here.
def index(request):
    projects_list = Project.objects.all()
    context = {
        'projects': projects_list
    }
    print(projects_list)
    return render(request, "projects/project.html", context)

def update(request, num):
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

    if request.method == "POST":
        print("GREAT SUCCESS 2")

        proj_updating = Project.objects.get(projectnumber = num)
        form = ProjectForm(request.POST, instance=proj_updating)
        if form.is_valid():
            form.save()
        return redirect('/projects')




def create(request):
    #Processing POST method (form to create a project)
    if request.method == "POST":
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
            #adding the new project to the database
            new_project.save()
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

    project.save()
    #switch value base on current value


    return HttpResponse("Successfully sent request, but did you send data??")
