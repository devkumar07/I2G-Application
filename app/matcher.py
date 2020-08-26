import sys
import math
import csv

from write import *

# matcher methods


def set_net_score(student_arr):
    for student in student_arr:
        student.net_score = sum(student.preferances)


def get_net_score(student):
    return student.net_score


def sort_by_net_score(student_arr):
    student_arr.sort(key=get_net_score)


def sort_by_preferance(student):
    sorted_project_preferances = []

    # replace later with a list of projects that is initialized from reading project roster
    for i in range(len(student.preferances)):
        sorted_project_preferances.append(i+1)

    # sort
    temp = student.preferances.copy()

    for i in range(len(temp)):

        min_idx = i
        for j in range(i+1, len(temp)):
            if temp[min_idx] > temp[j]:
                min_idx = j

        temp[i], temp[min_idx] = temp[min_idx], temp[i]
        sorted_project_preferances[i], sorted_project_preferances[
            min_idx] = sorted_project_preferances[min_idx], sorted_project_preferances[i]

    sorted_project_preferances.reverse()
    student.sorted_project_preferances = sorted_project_preferances


def space_available(project):       
    if len(project.students) < project.size:
        return True
    else:
        return False

def class_full(project):
    full = True
    for p in project:
        if len(project.students) < project.size:
            full = False
    return full


def remove_duplicates(student_arr):
    temp = student_arr
    for student in student_arr:
        for student_temp in temp:
            if student.email == student_temp.email and student_arr.index(student) != temp.index(student_temp):
                temp.pop(temp.index(student_temp))
    student_arr = temp


def match(student_arr, project_arr,destination):
    # sort students by net score
    set_net_score(student_arr)
    sort_by_net_score(student_arr)

    # remove duplictes
    remove_duplicates(student_arr)

    # find and apply size of each project
    size = 3

    for project in project_arr:
        project.size = size
        project.students = []

    # populate students in project based of preferances
    for student in student_arr:
        sort_by_preferance(student)
        for i in student.sorted_project_preferances:

            if i != -1:    
                if space_available(project_arr[i-1]) :
                    project_arr[i-1].students.append(student)
                    break
                elif class_full(project_arr):
                    project_arr[i-1].students.append(student)
                    break

    write_projects_csv(project_arr, destination)
