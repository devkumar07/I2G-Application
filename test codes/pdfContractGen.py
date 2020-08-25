import csv
from fpdf import FPDF


class csvProjectInfo(object):
    def __init__(self, client_FirstName, client_LastName, client_Email, client_OrganizationName, project_ID, project_TeamNumber, project_Title):
        self.client_FirstName = client_FirstName
        self.client_LastName = client_LastName
        self.client_Email = client_Email
        self.client_OrganizationName = client_OrganizationName
        self.project_ID = project_ID
        self.project_TeamNumber = project_TeamNumber
        self.project_Title = project_Title


class csvStudentInfo(object):
    def __init__(self, student_Timestamp, student_FirstName, student_LastName, student_Email):
        self.student_Timestamp = student_Timestamp
        self.student_FirstName = student_FirstName
        self.student_LastName = student_LastName
        self.student_Email = student_Email


def printContract(studentLists, projectLists):
    # creating the pdf document
    pdf = FPDF(format='letter', unit='in')
    pdf.add_page()
    pdf.set_font('Times', '', 10.0)
    effectivePageWidth = pdf.w - 2*pdf.l_margin

    # contract text
    pdf.multi_cell(effectivePageWidth, 0.15,
                   f'Dear {projectLists.client_FirstName},')
    pdf.multi_cell(effectivePageWidth, 0.15,
                   'These students digitally signed the IP+NDA agreement "UC Merced Innovate to Grow Program - Student Registration and Agreement" with UC Merced ID credentials:')
    pdf.multi_cell(effectivePageWidth, 0.15, '\n')

    # student information table
    studentTableTitle = ['Timestamp', 'First Name', 'Last Name', 'Email']
    th = pdf.font_size
    columnWidth = effectivePageWidth/4

    for row in studentTableTitle:
        # enters data in columns
        pdf.set_font('Times', 'B', 10.0)
        pdf.cell(columnWidth, th, str(row), border=2)
    pdf.ln(th)
    for eachStudent in studentLists:
        pdf.set_font('Times', '', 10.0)
        finalList = [eachStudent.student_Timestamp, eachStudent.student_FirstName,
                     eachStudent.student_LastName, eachStudent.student_Email]
        for datum in finalList:
            pdf.cell(columnWidth, th, str(datum), border=2)
        pdf.ln(th)

    # new line
    pdf.multi_cell(effectivePageWidth, 0.15, '\n')

    # project information table
    projectTable = [['Project ID:', projectLists.project_ID],
                    ['Project Title:', projectLists.project_Title, ],
                    ['Team #:', projectLists.project_TeamNumber],
                    ['Organization:', projectLists.client_OrganizationName],
                    ['Primary Contact First Name:', projectLists.client_FirstName],
                    ['Primary Contact Last Name:', projectLists.client_LastName],
                    ['Primary Conract Email:', projectLists.client_Email]]

    for projectData in projectTable:
        for projectInfo in projectData:
            pdf.cell(columnWidth, th, str(projectInfo), border=2)
        pdf.ln(th)

    # contract text cont.
    pdf.multi_cell(effectivePageWidth, 0.15, '\n')
    pdf.multi_cell(effectivePageWidth, 0.15, '''We have a digital record and timestamp of their agreement: the table above includes their credentials and time of acceptance. For your reference this is the language of the agreement that the students digitally signed.
Thank you for your participation in the Innovate to Grow program. Please let us know if you have any questions, or special circumstances to address.
Stefano Foresti
+1-801-971-3680
Stefano.Foresti@UCMerced.edu
University of California Merced, Director of Innovation -> engineering.ucmerced.edu ''')
    pdf.ln(0.5)

    # saves as filename
    pdf.output('contracts.pdf', 'F')
