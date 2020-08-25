from file_reader import *
import csv

"""
This functionality does the following:
    1) Remove all the entries where students have disagreed 
    2) Keep the updated responses based on timestamp
"""
def remove_incomplete_entries(clean_data):
    new_clean_data = clean_data
    i = 0 
    while i < len(new_clean_data):
        if str(new_clean_data[i].status) != "1":
            del new_clean_data[i]
        else:
            i = i + 1
    return new_clean_data

def remove_disagreed_students(clean_data):
    new_clean_data = clean_data
    i = 0 
    while i < len(new_clean_data):
        if str(new_clean_data[i].agreement) != "I agree":
            del new_clean_data[i]
        else:
            i = i + 1
    return new_clean_data

def remove_duplicate_entries(clean_data):
    new_clean_data = clean_data
    i = 0
    while i < len(new_clean_data):
        duplicate = False
        s = new_clean_data[i]
        k = i + 1
        while k < len(new_clean_data):
            sub_student = new_clean_data[k]
            if sub_student.email == s.email and sub_student.status == "1":
                del new_clean_data[i]
                duplicate = True
                break
            k = k + 1
        if duplicate == False:
            i = i + 1
    return new_clean_data

def clean_data_students(qualtrics):
    new_clean_data = remove_incomplete_entries(qualtrics)
    new_clean_data = remove_disagreed_students(new_clean_data)
    new_clean_data = remove_duplicate_entries(new_clean_data)
    return new_clean_data
