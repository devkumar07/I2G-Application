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
import unittest

class testApp(unittest.TestCase):
   
   def test_qualtrics_data_processing_functionality(self):
      students = read_students_new('data/input/Test_data/student_data1.csv')
      projects = read_projects('data/input/Test_data/projects.csv')
      catcourse = read_catcources('data/input/Test_data/roster.csv')
      missing_students = ['dwilley','jroot']
      output = list_missing(catcourse,students)
      res = []
      for o in output:
         res.append(o.email)
      self.assertListEqual(res,missing_students)
      incomplete_students = ['ahales@ucmerced.edu', 'npooran@ucmerced.edu']
      output, clean_data = get_clean_incomplete_students(catcourse, students)
      res = []
      for o in output:
         res.append(o.email)
      self.assertListEqual(res,incomplete_students)


if __name__ == '__main__':
    unittest.main()