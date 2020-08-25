import csv

import missing_student

catcourse_file_name = "data/input/testcat.csv"
qualtrics_file_name = "data/input/testqualtrics.csv"
catcourse = []
qualtrics = []

with open(qualtrics_file_name, 'r', encoding='utf-8-sig') as csvfile:
    csvread = csv.reader(csvfile)
    for row in csvread:
        temp = []
        for data in row:
            temp.append(data)
        qualtrics.append(missing_student(temp[0]+''+temp[1],temp[2]))
with open(catcourse_file_name, 'r', encoding='utf-8-sig') as csvfile:
    csvread = csv.reader(csvfile)
    for row in csvread:
        temp = []
        for data in row:
            temp.append(data)
        catcourse.append(missing_student(temp[0],temp[1]))


l1=list_missing(catcourse,qualtrics)
export_list(l1)
