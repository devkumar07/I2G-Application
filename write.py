import csv
from fpdf import FPDF

def write_projects_csv(project_arr):
    
    with open('data/output/student-project.csv', 'w') as f:
        writer = csv.writer(f)
        for project in project_arr:
            writer.writerow(['Project',project.project_id])
            for student in project.students:
                writer.writerow([student.first_name,student.last_name, student.email])
            writer.writerow("\n")

def write_project_pdf_contract(project):
    # creating the pdf document
    pdf = FPDF(format='letter', unit='in')
    pdf.add_page()
    pdf.set_font('Times', '', 10.0)
    effectivePageWidth = pdf.w - 2*pdf.l_margin

    # contract text
    pdf.multi_cell(effectivePageWidth, 0.15,
                   f'Dear {project.client_first_name},')
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
    
    for student in project.students:
        pdf.set_font('Times', '', 10.0)
        finalList = [student.timestamp, student.first_name,
                     student.last_name, student.email]
        for datum in finalList:
            pdf.cell(columnWidth, th, str(datum), border=2)
        pdf.ln(th)

    # new line
    pdf.multi_cell(effectivePageWidth, 0.15, '\n')

    # project information table
    projectTable = [['Project ID:', project.project_id],
                    ['Project Title:', project.project_title, ],
                    ['Team #:', 'needs to be added'],
                    ['Organization:', project.client_organization_name],
                    ['Primary Contact First Name:', project.client_first_name],
                    ['Primary Contact Last Name:', project.client_last_name],
                    ['Primary Conract Email:', project.client_email]]

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
    pdf.output('data/output/contracts/2019-July-Fall-CAP-StudentAgreement-Team'+project.project_TeamNumber+'-'+project.client_OrganizationName+'-'+project.project_ID+'.pdf','F')