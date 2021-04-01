from datetime import datetime


class Mapper:
    __instance = None
    __date_format = '%Y-%m-%d'  # YYYY-MM-DD
    __date_time_format = '%Y-%m-%d_%H:%M:%S'  # YYYY-MM-DD_hh:mm:ss

    def __init__(self):
        Mapper.__instance = self

    @staticmethod
    def get_instance():
        if Mapper.__instance is None:
            return Mapper()
        return Mapper.__instance

    @staticmethod
    def get_date_format():
        return Mapper.__date_format

    @staticmethod
    def get_date_time_format():
        return Mapper.__date_time_format

    def json_to_date(self, json):
        return datetime.strptime(json, Mapper.__date_format)

    def json_to_date_time(self, json):
        return datetime.strptime(json, Mapper.__date_time_format)

    def json_to_client(self, json):
        from domain.client import Client
        return json if json is None else Client(json['id'], json['name'], "" if json['description'] is None else json['description'])

    def json_to_department(self, json):
        from domain.department import Department
        return json if json is None else Department(json['id'], json['name'], "" if json['description'] is None else json['description'])

    def json_to_user(self, json):
        from domain.user import User
        return json if json is None else \
            User(json['id'], json['name'], json['email'], None, json['role'],
                 json['seniorityLevel'],
                 json['departmentId'])

    def json_to_project(self, json):
        from domain.project import Project
        return json if json is None else Project(json['id'], json['name'],
                       "" if json['description'] is None else json['description'],
                       datetime.strptime(json['startDate'], Mapper.__date_format),
                       None if json['endDate'] is None else datetime.strptime(json['endDate'], Mapper.__date_format),
                       datetime.strptime(json['deadlineDate'], Mapper.__date_format), json['clientId'])


    def json_to_technologies(self, json):
        from domain.technology import Technology
        techs = []
        for x in json['technologies']:
            id = None if 'id' not in x else x['id']
            techs.append(Technology(id, x['name']))
        return techs

    def json_to_reports(self, json):
        from domain.report import Report
        reports = []
        for x in json['reports']:
            reports.append(Report(None, x['user_id'], x['skill_id'], x['project_id'], x['mark'], None))
            # 'id' si 'date' nu vin de la client
        return reports

    def client_to_json(self, client):
        return client if client is None else {'id': client.id, 'name': client.name, 'description': client.description}

    def department_to_json(self, department):
        return department if department is None else {'id': department.id, 'name': department.name,
                                                      'description': department.description}


    def user_to_json(self, user, department=None,nrofprojects=None):
        return user if user is None else {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'seniorityLevel': user.seniority_level,
            'departmentId': user.department_id,
            'department': department,
            'nrOfProjects' : nrofprojects
        }

    def project_to_json(self, project, employees=None, technologies=None, client=None):
        return project if project is None else {
            'id': project.get_id(),
            'name': project.get_name(),
            'description': project.get_description(),
            'startDate': project.get_start_date().strftime(Mapper.__date_format),
            'endDate': None if project.get_end_date() is None else project.get_end_date().strftime(Mapper.__date_format),
            'deadlineDate': project.get_deadline_date().strftime(Mapper.__date_format),
            'clientId': project.get_client_id(),
            'employees': employees,
            'technologies': technologies,
            'client': client
        }


    def technology_to_json(self, tech):
        return {'id': tech.get_id(), 'name': tech.get_name()}

    def report_session_to_json(self, rs, project):
        return {'id': rs.get_id(),
                'start_date': rs.get_start_date().strftime(Mapper.__date_format),
                'end_date': rs.get_end_date().strftime(Mapper.__date_format),
                'was_completed': rs.get_was_completed(), 'user_id': rs.get_user_id(),
                'project': self.project_to_json(project)
        }

    def skill_to_json(self, skill):
        return {'id': skill.get_id(), 'name': skill.get_name()}
