import csv
from matcher import *
from project import *
from student import *
from missing_student import *
from write import *
from new_student import *


students_file_name = "data/input/Test_data/student_data1.csv"
test_data = "data/input/Test_data/student_data1.csv"
projects_file_name = 'data/input/Test_data/projects.csv'
catcourse_file_name = "data/input/Test_data/roster.csv"
qualtrics_file_name = "data/input/Student_final_roster_missing.csv"
matched_students = "data/output/student-project.csv"
destination_matcher = "data/output/student-project.csv"
destination_gsheet_matcher = 'students-matched'
destination_missing_student = "data/output"
destination_contracts = "data/output/contracts/"
students = []
students1 = []
projects = []
catcourse = []
students2 = []
projects2 = []
choice = input("1. Match \n2. Find missing students \n3. Generate contracts\n")
# read csv files
with open(students_file_name, 'r', encoding= 'utf-8-sig') as csvfile:
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

        students.append(new_Student(row[0], row[1], row[2], row[3], row[4], row[9], temp))
with open(projects_file_name, 'r', encoding='utf-8-sig') as csvfile:
    # create csvread obj
    csvread = csv.reader(csvfile)
    # populate projects
    for row in csvread:
        projects.append(Project(row[0], row[3], row[4], row[5], row[6], row[9]))
with open(catcourse_file_name, 'r', encoding='utf-8-sig') as csvfile:
    # create csvread obj
    csvread = csv.reader(csvfile)
    temp = []
    # populate projects
    for row in csvread:
        catcourse.append(Student(0,row[0],0, row[1],0,temp))
with open(test_data, 'r', encoding= 'utf-8-sig') as csvfile:
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

        students1.append(new_Student(row[0], row[1], row[2], row[3], row[4], row[9], temp))
if choice == '1':
    match(students,projects,destination_gsheet_matcher)
if choice == '2':
    missing_student, incomplete_data, clean_data, disagreed_students = list_missing(catcourse,students1)
    export_missing_students(missing_student, incomplete_data, disagreed_students,destination_missing_student)
if choice == '3':
    with open(matched_students, 'r', encoding='utf-8-sig') as csvfile:
        # create csvread obj
        csvread = csv.reader(csvfile)
        temp = []
        # populate projects
        for row in csvread:
            students2.append(Student(row[0], row[1], row[2],row[3],row[4],0))
            projects2.append(Project(row[5],row[6],row[7],row[8],row[9],row[10]))
        t = 1
        p = 1
        projects2 = list(dict.fromkeys(projects2))
        project_list = []
        while t <= 10:
            student_list = []
            for student in students2:
                if str(t) == student.contract:
                    student_list.append(student)
            write_project_pdf_contract(student_list, projects2[p],t,destination_contracts)
            t += 1
            p += len(student_list)

if choice == '4':
    write_project_information('source','destination')
