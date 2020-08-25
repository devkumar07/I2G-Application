import csv
from student import *
from new_student import *
from project import *
from write import *
from qualtrics_data_processing import *
from Team import *

#adding comments
def read_students(file):
    students = []
    bad_data = []
    # read csv files
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        # create csvread obj
        csvread = csv.reader(csvfile)
        # populate students with Student obj

        for row in csvread:
            temp = []
            # convert string preferances into numericals
            for pref in row[14:]:
                if pref == '5':
                    temp.append(5)
                elif pref == '4':
                    temp.append(4)
                elif pref == '3':
                    temp.append(3)
                elif pref == '2':
                    temp.append(2)
                elif pref == '1':
                    temp.append(1)
                else:
                    temp.append(-1)

            if row[1]==str(1):
                students.append(Student(row[0], row[2], row[3], row[4], row[9], temp))
            else:
                bad_data.append(Student(0, row[2], row[3], row[4], 0, 0))

    return students, bad_data

# This definition is for testing purposes for the catcours-qualtrics students
def read_students_new(file):
    students = []
    # read csv files
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        # create csvread obj
        csvread = csv.reader(csvfile)
        # populate students with Student obj

        for row in csvread:
            temp = []
            # convert string preferances into numericals
            for pref in row[14:]:
                if pref == '5':
                    temp.append(5)
                elif pref == '4':
                    temp.append(4)
                elif pref == '3':
                    temp.append(3)
                elif pref == '2':
                    temp.append(2)
                elif pref == '1':
                    temp.append(1)
                else:
                    temp.append(-1)
            students.append(new_Student(row[0], row[1], row[2], row[3], row[4], row[9], temp, False))

    return students

def read_projects(file):

    projects = []

    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        # create csvread obj
        csvread = csv.reader(csvfile)
        # populate projects
        for row in csvread:
            projects.append(
                Project(row[0], row[3], row[4], row[5], row[6], row[9]))

    return projects


def read_catcources(file):

    catcourse = []

    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        # create csvread obj
        csvread = csv.reader(csvfile)
        temp = []
        # populate projects
        for row in csvread:
            catcourse.append(Student(0,row[0], 0, row[1],0,temp))

    return catcourse

def read_matched_students(file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        # create csvread obj
        csvread = csv.reader(csvfile)
        t = 0
        line_count = 0
        teams = []
        team_number = ''
        project_id = ''
        organization_name = ''
        client_first_name = ''
        client_last_name = ''
        client_email =''
        project_title = ''
        studs = []
        for row in csvread:
            if line_count == 0:
                line_count = line_count + 1
            else:
                if t != int(row[4]):
                    if t != 0: 
                        team = Team(Project(project_id,organization_name,client_first_name, client_last_name,client_email,project_title),studs,team_number)
                        teams.append(team)
                    studs = []
                    t = int(row[4])
                    team_number = str(t)
                    project_id = row[5]
                    organization_name = row[6]
                    client_first_name = row[7]
                    client_last_name = row[8]
                    client_email = row[9]
                    project_title = row[10]
                studs.append(new_Student(row[0],'1',row[1],row[2],row[3],'Yes','n/a',True))
                line_count = line_count + 1
        team = Team(Project(project_id,organization_name,client_first_name, client_last_name,client_email,project_title),studs,team_number)
        teams.append(team)
        return teams 
                    
#This function attempts to read the projects from projects log and write it in another gsheet
def get_projects_semester(source,destination,semester):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json',scope)
    client = gspread.authorize(creds)
    source_sheet = client.open(source).sheet1
    destination_sheet = client.open(destination).sheet1
    semesters = source_sheet.findall(semester)
    team = 1
    destination_sheet.append_row(['Project ID','Team Number','Time Submitted','Organization Name','Primary Contact First Name','Primary Contact Last Name','Primary Contact Email','Project Title','Background','Problem','Objective'])
    for i in range(0,len(semesters)):
        row = semesters[i].row
        destination_sheet.append_row([source_sheet.cell(row,1).value,team,'',source_sheet.cell(row,10).value,source_sheet.cell(row,11).value,source_sheet.cell(row,12).value,source_sheet.cell(row,16).value,source_sheet.cell(row,17).value,source_sheet.cell(row,18).value,source_sheet.cell(row,19).value,source_sheet.cell(row,20).value])
        team = team + 1

