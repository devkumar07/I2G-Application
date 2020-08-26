class Team(object):
    def __init__(self, project, students, team_number):
        self.project = project
        self.students = students
        self.team_number = team_number

    #This function prints the team array
    def print_team_info(self):
        print('-----')
        print(self.project.project_title)
        for s in self.students:
            print(s.email)
        print('-----')