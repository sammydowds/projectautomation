import xlrd
from datetime import datetime


#function pulls projects, and appends a list of dictionaries with each dictionary being a project
def list_projects():
    #opening xlsx sheet and saving to a var
    book = xlrd.open_workbook("projects/projects2.xlsx")

    #saving the second sheet (data)
    data = book.sheet_by_index(1)

    #appending the rows into a list of projects
    project = []
    for rx in range(data.nrows):
        project_created = []
        for element in data.row(rx):
            project_created.append(element.value)
        project.append(project_created)

    #filtering for projects with real numbers, and converting the dates to tuple
    real_project = []
    for proj in project:
        proj = proj[1:23]
        del proj[1:7]
        del proj[2:4]
        del proj[10]
        for p in range(2,13):
            if type(proj[p]) == float and proj[p] != None:
                proj[p] = xlrd.xldate_as_tuple(proj[p], 0)
        if isinstance(proj[0], float):
            real_project.append(proj)

    #assembling a dictionary for each project, and giving a key to each value
    object_vars = ['projectnumber', 'projectname', 'mechanicalrelease', 'electricalrelease', 'manufacturing', 'finishing', 'assembly', 'integration', 'internalrunoff', 'customerrunoff', 'ship', 'installstart', 'installfinish', 'documentation']
    object_dictionary = []
    for p in real_project:
        temp_dict = {}
        temp_dict[object_vars[0]] = p[0]
        temp_dict[object_vars[1]] = p[1]
        for i in range(2, 13):
            #removing blank dates
            if isinstance(p[i], tuple):
                print(p[i])
                temp_dict[object_vars[i]]=(str(p[i][0]) +'-'+str(p[i][1])+'-'+str(p[i][2]))
        temp_dict['engineering_start'] = datetime(2019, 2, 1)
        object_dictionary.append(temp_dict)

    for proj in object_dictionary:
        proj['projectnumber'] = proj['projectnumber'] * 100
    print(object_dictionary)


    return object_dictionary
