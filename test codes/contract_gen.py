import csv
from fpdf import FPDF

class csvProjectInfo(object):
    def __init__(self, client_FirstName, client_LastName, client_Email,client_OrganizationName, project_ID, project_TeamNumber,project_Title):
        self.client_FirstName = client_FirstName
        self.client_LastName = client_LastName
        self.client_Email = client_Email
        self.client_OrganizationName = client_OrganizationName
        self.project_ID = project_ID
        self.project_TeamNumber = project_TeamNumber
        self.project_Title = project_Title

class csvStudentInfo(object):
    def __init__(self,student_Timestamp,student_FirstName,student_LastName,student_Email):
        self.student_Timestamp = student_Timestamp
        self.student_FirstName = student_FirstName
        self.student_LastName = student_LastName
        self.student_Email = student_Email

def printContract(studentLists,projectLists):
    # from fpdf import FPDF
    pdf = FPDF(format = 'letter', unit = 'in')
    pdf.add_page()
    pdf.set_font('Times','',10.0)
    effectivePageWidth = pdf.w - 2*pdf.l_margin

    # contract text
    pdf.multi_cell(effectivePageWidth, 0.15,f'Dear {projectLists.client_FirstName},')
    pdf.multi_cell(effectivePageWidth, 0.15,'These students digitally signed the IP+NDA agreement "UC Merced Innovate to Grow Program - Student Registration and Agreement" with UC Merced ID credentials:')
    pdf.multi_cell(effectivePageWidth, 0.15,'\n')

    # student information table
    studentTableTitle = ['Timestamp', 'First Name', 'Last Name', 'Email']
    th = pdf.font_size
    columnWidth = effectivePageWidth/4

    for row in studentTableTitle:
        # enters data in columns
        pdf.set_font('Times','B',10.0)
        pdf.cell(columnWidth, th, str(row), border = 2)
    pdf.ln(th)
    for eachStudent in studentLists:
        pdf.set_font('Times','',10.0)
        finalList = [eachStudent.student_Timestamp, eachStudent.student_FirstName, eachStudent.student_LastName, eachStudent.student_Email]
        for datum in finalList:
            pdf.cell(columnWidth, th, str(datum), border = 2)
        pdf.ln(th)

    # new line
    pdf.multi_cell(effectivePageWidth, 0.15,'\n')

    # project information table
    projectTable = [['Project ID:', projectLists.project_ID],
    ['Project Title:', projectLists.project_Title,],
    ['Team #:', projectLists.project_TeamNumber],
    ['Organization:', projectLists.client_OrganizationName],
    ['Primary Contact First Name:', projectLists.client_FirstName],
    ['Primary Contact Last Name:', projectLists.client_LastName],
    ['Primary Conract Email:', projectLists.client_Email]]

    for projectData in projectTable:
        for projectInfo in projectData:
            pdf.cell(columnWidth,th,str(projectInfo),border = 2)
        pdf.ln(th)

    # contract text cont.
    pdf.multi_cell(effectivePageWidth, 0.15,'\n')
    pdf.multi_cell(effectivePageWidth, 0.15,'''We have a digital record and timestamp of their agreement: the table above includes their credentials and time of acceptance. For your reference this is the language of the agreement that the students digitally signed.
Thank you for your participation in the Innovate to Grow program. Please let us know if you have any questions, or special circumstances to address.
Stefano Foresti
+1-801-971-3680
Stefano.Foresti@UCMerced.edu
University of California Merced, Director of Innovation -> engineering.ucmerced.edu ''')
    pdf.ln(0.5)
    pdf.output('data/output/contracts/2019-July-Fall-CAP-StudentAgreement-Team'+projectLists.project_TeamNumber+'-'+projectLists.client_OrganizationName+'-'+projectLists.project_ID+'.pdf','F')

def main():

    projectList = []
    studentList = []
    studentArray = []
    TEST = []

    #projectIDLocater = input('Enter the project ID: ')
    #TeamNumberLocater = input('Enter the project team number: ')

    projects = open('data/input/projectsTEST.csv','r',encoding = "utf8")
    students = open('data/input/studentsTEST.csv','r',encoding = "utf8")

    # count for creating  projectList
    count = 0

    # parsing the csv file
    with projects as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            data = [row for row in csv.reader(csvDataFile)]
            for i in data:
                # if projectIDLocater == i[0]:
                # if TeamNumberLocater == i[1]:
                client_FirstName = i[4]
                client_LastName = i[5]
                client_Email = i[6]
                client_OrganizationName = i[3]

                project_ID = i[0]
                project_Title = i[17]
                project_TeamNumber = i[1]
                projectList.append(csvProjectInfo(client_FirstName, client_LastName, client_Email,client_OrganizationName, project_ID, project_TeamNumber,project_Title))
                """
                if count > 0:
                    # appending a lists for the respective projectID
                    projectList.append(csvProjectInfo(client_FirstName, client_LastName, client_Email,client_OrganizationName, project_ID, project_TeamNumber,project_Title))

                count = count + 1
                """
    with students as csvDataFile1:
        csvReader1 = csv.reader(csvDataFile1)
        for row1 in csvReader1:
            data1 = [row1 for row1 in csvReader1]
        TeamNumberLocater = 1
        while TeamNumberLocater < len(projectList):
            for n in data1:
                if str(TeamNumberLocater) == n[7]:
                    student_Timestamp = n[0]
                    student_FirstName = n[1]
                    student_LastName = n[2]
                    student_Email = n[3]
                    studentArray.append(csvStudentInfo(student_Timestamp,student_FirstName,student_LastName,student_Email))
            printContract(studentArray,projectList[TeamNumberLocater])
            TeamNumberLocater+= 1
            studentArray = []

            # for eachStudent in studentArray:
                # eachStudent.printStuff1()




        # studentArray.printStuff1()

        # projectList[12].printStuff()



main()
