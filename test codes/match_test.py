import csv

from matcher import *
from project import *
from student import *
from write import *

students_file_name = "data/input/Student_final_roster.csv"
projects_file_name = 'data/input/projects.csv'
students = []
projects = []

# read csv files
with open(students_file_name, 'r', encoding='utf-8-sig') as csvfile:
    # create csvread obj
    csvread = csv.reader(csvfile)
    # populate students with Student obj
    for row in csvread:
        temp = []
        # convert string preferances into numericals
        for pref in row[14:]:
            if pref == 'Definitely yes':
                temp.append(5)
            elif pref == 'Probably yes':
                temp.append(4)
            elif pref == 'Maybe':
                temp.append(3)
            elif pref == 'Probably not':
                temp.append(2)
            else:
                temp.append(1)

        students.append(Student(row[0], row[2], row[3], row[4], row[9], temp))

with open(projects_file_name, 'r', encoding='utf-8-sig') as csvfile:
    # create csvread obj
    csvread = csv.reader(csvfile)
    # populate projects
    for row in csvread:
        projects.append(
            Project(row[0], row[3], row[4], row[5], row[6], row[9]))

match(students, projects)

for student in students:
    print(student.first_name)
    print(student.net_score)
    print(student.preferances)
    print(student.sorted_project_preferances)
    print("\n")

for project in projects:
    print(project.project_id + "\t" + project.project_title)
    print(project.size)
    for student in project.students:
        print(student.first_name + "\t\t" + student.email)
    print("\n")

write_project_pdf_contract(projects[1])
