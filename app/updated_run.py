import csv
from matcher import *
from project import *
from student import *
from qualtrics_data_processing import *
from write import *
from file_reader import *
from new_matcher import *
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.flow import *
from networkx.algorithms.bipartite import hopcroft_karp_matching
from Team import *
from data_cleanup import *

students = read_students_new('data/input/Test_data/student_data1.csv')
projects = read_projects('data/input/Test_data/projects.csv')
catcourse = read_catcources('data/input/Test_data/roster.csv')

missing_students = list_missing(catcourse, students)
incomplete_data, clean_data = get_clean_incomplete_students(catcourse, students)
disagreed_students = find_disagreed_students(catcourse, students)
export_missing_students(missing_students,incomplete_data,disagreed_students,'data/output')

clean_data = clean_data_students(students)
teams = match_students(clean_data,projects)

write_projects_csv(teams,'data/output')

#write_project_pdf_contract(teams,'data/output/contracts/')



"""
Testing the writing Projects log 
source = 'sample projects log'
semester = '2019-08-Fall-CAP'
destination = 'projects-API'
get_projects_semester(source,destination,semester)
"""

