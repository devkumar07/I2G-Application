import csv
from data_cleanup import clean_data_students

def list_missing(catcourse, qualtrics):
    #Checking whether a student has not at all done qualtrics 
    qualtrics = clean_data_students(qualtrics)
    missing_student = [] 
    for student in catcourse:
        student_exists = False
        catcourse_email = student.email
        for qualtrics_student in qualtrics:
            if qualtrics_student.email[0:(len(qualtrics_student.email)-13)] == catcourse_email:
                student_exists = True
        if student_exists == False:
            missing_student.append(student)
    return missing_student
    
# Pre-clean qualtrics data (Differentiating incomplete from complete)
def get_clean_incomplete_students(catcourse, qualtrics):
    qualtrics = clean_data_students(qualtrics)
    incomplete_data = []
    clean_data = []
    for student in qualtrics:
        if student.status != str(1):
            duplicate_entry = False
            for dup_student in qualtrics:
                if dup_student.email == student.email and dup_student.status == str(1):
                    duplicate_entry = True
            if duplicate_entry == False:
                incomplete_data.append(student)
        else:
            clean_data.append(student)
    return incomplete_data, clean_data
    
# Looking for agreement and non-agreement students
def find_disagreed_students(catcourse,qualtrics):
    qualtrics = clean_data_students(qualtrics)
    disagreed_students = []
    for student in qualtrics:
        if student.agreement != "I agree":
            disagreed_students.append(student)

    return disagreed_students