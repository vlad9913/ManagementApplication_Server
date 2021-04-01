from datetime import datetime, date, timedelta

from controller.helpers.mapper import Mapper


class ProjectService:
    def __init__(self, __repo, project_technology_repo, user_project_repo, technology_service, user_service,
                 client_service):
        self.__project_repo = __repo
        self.__project_tech_repo = project_technology_repo
        self.__user_project_repo = user_project_repo
        self.__tech_service = technology_service
        self.__user_service = user_service
        self.__client_service = client_service

    def getAllProjects(self):
        return self.__project_repo.getAll()

    def getOneProject(self, id):
        project = self.__project_repo.getOne(id)
        if project is None:
            raise ValueError("The project with the given ID does not exist.")
        return project

    def addProject(self, project):
        p = self.__project_repo.getOne(project.get_id())
        if p is not None:
            raise ValueError("A project with the given ID already exists.")
        self.__client_service.getOne(project.get_client_id())  # Throws ValueError if client does not exist
        return self.__project_repo.add(project)

    def removeProject(self, id):
        project = self.__project_repo.getOne(id)
        if project is None:
            raise ValueError("The project with the given ID does not exist.")
        for x in self.getTechnologiesForProject(project.get_id()):
            self.unassignTechFromProject(project.get_id(), x.get_id())
        for x in self.getUsersForProject(project.get_id()):
            self.unassignUserFromProject(project.get_id(), x.get_id())

        from controller.feedback_controller import feedback_service
        feedback_service.forceDeleteFeedbackDataForProject(project.get_id())

        self.__project_repo.remove(project)

    def updateProject(self, project):
        p = self.__project_repo.getOne(project.get_id())
        if p is None:
            raise ValueError("The project with the given ID does not exist.")
        if p.get_client_id() != project.get_client_id():
            self.__client_service.getOne(project.get_client_id())  # Throws ValueError if client does not exist
        return self.__project_repo.update(project)

    def assignTechToProject(self, projectId, tech):
        from domain.project_technology import Project_Technology
        self.getOneProject(projectId)  # raises ValueError if project with given ID does not exist
        try:
            self.__tech_service.getOne(tech.get_id())
        except ValueError:
            self.__tech_service.add(tech)  # Daca technologia nu exista o adaug

        self.__project_tech_repo.add(Project_Technology(projectId, tech.get_id()))
        return tech

    def unassignTechFromProject(self, projectId, techId):
        pt = self.__project_tech_repo.getOne(projectId, techId)
        if pt is None:
            raise ValueError("Technology was not assigned to project")

        self.__project_tech_repo.remove(pt)

        if not self.__project_tech_repo.getAllForTechnology(techId):  # Lista goala
            self.__tech_service.remove(techId)

    def isTechAssignedToProject(self, projectId, techId):
        return self.__project_tech_repo.getOne(projectId, techId) is not None

    def assignUserToProject(self, projectId, userId):
        from domain.user_project import User_Project
        self.getOneProject(projectId)
        self.__user_service.getOne(userId)
        self.__user_project_repo.add(User_Project(userId, projectId))

    def unassignUserFromProject(self, projectId, userId):
        up = self.__user_project_repo.getOne(userId, projectId)
        if up is None:
            raise ValueError("User was not assigned to project")
        self.__user_project_repo.remove(up)

    def isUserAssignedToProject(self, projectId, userId):
        return self.__user_project_repo.getOne(userId, projectId) is not None

    def getUsersForProject(self, projectId):
        self.getOneProject(projectId)  # raises ValueError if project with given ID does not exist

        return [self.__user_service.getOne(x.get_user_id()) for x in
                self.__user_project_repo.getAllForProject(projectId)]

    def getTechnologiesForProject(self, projectId):
        return [self.__tech_service.getOne(x.get_technology_id()) for x in
                self.__project_tech_repo.getAllForProject(projectId)]
        # raises ValueError if project with given ID does not exist

    def getProjectsForUser(self, userId):
        return [self.getOneProject(x.get_project_id()) for x in self.__user_project_repo.getAllForUser(userId)]
        # raises ValueError if project with given ID does not exist

    def getProjectsForTechnology(self, techId):
        return [self.getOneProject(x.get_project_id()) for x in self.__project_tech_repo.getAllForTechnology(techId)]
        # raises ValueError if project with given ID does not exist

    def get_technologies_and_users_with_recommandation(self):
        technologies = []
        for technology in self.__tech_service.getAll():
            technology = Mapper.get_instance().technology_to_json(technology)
            technology['users'] = []
            for user in self.__user_service.getAll():
                experience_in_days = 0
                for user_project in self.__user_project_repo.getAllForUser(user.id):
                    project = self.__project_repo.getOne(user_project.project_id)
                    project_technology = self.__project_tech_repo.getOne(project.id, technology['id'])
                    if project_technology is not None:
                        difference = (
                                         datetime.now().date() if project.end_date is None else project.end_date) - project.start_date
                        experience_in_days += difference.days

                technology['users'].append({
                    'id': user.id,
                    'name': user.name,
                    'experienceInDays': experience_in_days
                })

            technologies.append(technology)

        return technologies
