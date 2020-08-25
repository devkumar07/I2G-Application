import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fpdf import FPDF, HTMLMixin
import pprint

class MyFPDF(FPDF, HTMLMixin):
    pass

def write_projects_csv(teams, destination):

    with open(destination + '/match_result.csv', 'w', encoding='utf-8-sig', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'First Name', 'Last Name', 'Email', 'Team #', 'Project ID',
                         'Organization Name', 'Client First Name', 'Client Last Name', 'Client Email', 'Project Title'])
        for team in teams:
            students = team.students
            project = team.project
            for s in students:
                writer.writerow([s.timestamp, s.first_name, s.last_name, s.email, team.team_number, 
                project.project_id,project.client_organization_name, project.client_first_name, project.client_last_name, project.client_email,
                project.project_title])

def write_projects_gsheet(project_arr, destination):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json',scope)
    client = gspread.authorize(creds)
    sheet = client.open(destination).sheet1
    sheet.insert_row(['Timestamp', 'First Name', 'Last Name', 'Email', 'Team #', 'Project ID',
                     'Organization Name', 'Client First Name', 'Client Last Name', 'Client Email', 'Project Title'],1)
    team_number = 1
    index = 3
    for project in project_arr:
        for student in project.students:
            sheet.insert_row([student.timestamp, student.first_name, student.last_name, student.email, team_number, project.project_id,
                             project.client_organization_name, project.client_first_name, project.client_last_name, project.client_email, project.project_title],index)
            index = index + 1
        team_number = team_number + 1


def write_project_information(source, destination):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json',scope)
    client = gspread.authorize(creds)
    source_sheet = client.open(source).sheet1
    destination_sheet = client.open(destination).sheet1
    source_row = 2
    source_col = 3
    while source_sheet.cell(source_row, source_col).value != "":
        source_project_id = source_sheet.cell(source_row, source_col).value
        dest_row = 4 
        dest_col = 1
        while destination_sheet.cell(dest_row, dest_col).value != source_project_id:
            dest_row = dest_row + 1
        i = 1
        k = 22
        while i <= 4:
            data = source_sheet.cell(source_row,source_col+i).value
            destination_sheet.update_cell(dest_row,dest_col+k,data)
            k = k+1
            i = i+1
        source_row = source_row+1

def export_missing_students(missing_student,incomplete_data, disagreed_students, destination):
    with open(destination + '/missing_student.csv', 'w', encoding='utf-8-sig', newline = '') as f:
        writer = csv.writer(f)
        # Writing missing students information
        writer.writerow(['Students who have not finished qualtrics form'])
        writer.writerow(['First Name', 'Last Name', 'Email/UcmNetID'])
        for student in missing_student:
            writer.writerow(
                [student.first_name, student.last_name, student.email])
        writer.writerow('\n')
        # Writing Incomplete registration students information 
        writer.writerow(['Students who have incomplete qualtrics data and are not being considered for matching'])
        writer.writerow(['First Name', 'Last Name', 'Email/UcmNetID'])
        for student in incomplete_data:
            writer.writerow(
                [student.first_name, student.last_name, student.email])
        writer.writerow('\n')
        # Writing Disagreed students
        writer.writerow(['Students who have disagreed'])
        writer.writerow(['First Name', 'Last Name', 'Email/UcmNetID'])
        for student in disagreed_students:
            writer.writerow(
                [student.first_name, student.last_name, student.email])

def write_project_pdf_contract(teams, destination):
    for team in teams:
        #storing information in lists
        project = team.project
        students = team.students
        # creating the pdf document
        pdf = MyFPDF()
        pdf.add_page()
        pdf.set_font('Times', '', 10.0)
        effectivePageWidth = pdf.w - 2*pdf.l_margin

        # contract text
        pdf.multi_cell(effectivePageWidth, 0.15,
                    f'Dear {project.client_first_name},')
        pdf.write_html(
                    '<p><font size = 10 face="Times"> These <b>students digitally signed the IP+NDA agreement</b> "UC Merced Innovate to Grow Program - Student Registration and Agreement" with UC Merced ID credentials </font> </p>')
        pdf.multi_cell(effectivePageWidth, 10, '\n')

        # student information table
        studentTableTitle = ['Timestamp', 'First Name', 'Last Name', 'Email']
        th = pdf.font_size
        columnWidth = effectivePageWidth/4

        for row in studentTableTitle:
            # enters data in columns
            pdf.set_font('Times', 'B', 10.0)
            pdf.cell(columnWidth, th, str(row), border=2)
        pdf.ln(th)

        for student in students:
            pdf.set_font('Times', '', 10.0)
            finalList = [student.timestamp, student.first_name,
                        student.last_name, student.email]
            for datum in finalList:
                pdf.cell(columnWidth, th, str(datum), border=2)
            pdf.ln(th)

        # new line
        pdf.multi_cell(effectivePageWidth, 5, '\n')
        pdf.write_html('<p> <font size = 10 face="Times"> to <b>participate in your project:</b> </font></p>')
        pdf.multi_cell(effectivePageWidth, 10, '\n')
        pdf.set_font('Times', '', 10.0)
        # project information table
        projectTable = [['Project ID:', project.project_id],
                        ['Project Title:', project.project_title, ],
                        ['Team #:', str(team.team_number)],
                        ['Organization:', project.client_organization_name],
                        ['Primary Contact First Name:', project.client_first_name],
                        ['Primary Contact Last Name:', project.client_last_name],
                        ['Primary Conract Email:', project.client_email]]

        for projectData in projectTable:
            for projectInfo in projectData:
                pdf.cell(columnWidth, th, str(projectInfo), border=2)
            pdf.ln(th)

        # contract text cont.
        pdf.multi_cell(effectivePageWidth, 10, '\n')
        pdf.write_html('<p> <font size = 10 face="Times"><b>We have a digital record and timestamp of their agreement:</b> the table above includes their credentials and time of acceptance.</font> </p>')
        pdf.multi_cell(effectivePageWidth, 2, '\n')
        pdf.write_html('<p> <font size = 10 face="Times"><b>For your reference </b><a href = \'https://docs.google.com/document/d/1aj17d_u5Fir1_Q3TaTISZKyXnwN_JJkqdOux-TC_4ks/edit?usp=sharing\'><font size = 10 face="Times">this is the language </font></a>of the agreement that the students digitally signed.</font></p>')
        pdf.multi_cell(effectivePageWidth, 5, '\n')
        pdf.write_html('<p> <font size = 10 face="Times"> Thank you for your participation in the Innovate to Grow program. Please let us know if you have any questions, or special circumstances to address.</font></p>')
        pdf.multi_cell(effectivePageWidth, 10, '\n')
        pdf.set_font('Times', '', 10.0)
        pdf.multi_cell(effectivePageWidth, 5, 'Stefano Foresti\n+1-801-971-3680\nStefano.Foresti@UCMerced.edu\n University of California Merced, Director of Innovation -> engineering.ucmerced.edu')
        pdf.write_html('<p> <font size = 10 face="Times">website:<a href = \'https://docs.google.com/document/d/1aj17d_u5Fir1_Q3TaTISZKyXnwN_JJkqdOux-TC_4ks/edit?usp=sharing\'><font size = 8 face="Times">innovatetogrow.ucmerced.edu</font></a> </font> </p>')
        pdf.ln(1)

        # saves as filename
        pdf.output(destination+'/2020-Jan-Spring-CAP-StudentAgreement-Team'+str(team.team_number) +
                '-'+project.client_organization_name+'-'+project.project_id+'.pdf', 'F')
