from flask import Blueprint, Response
from flask import jsonify, request

from controller.helpers.authorize import auth_required_with_role
from controller.helpers.mapper import Mapper
from domain.enums.role import Role
from repository.project_repository import ProjectRepository
from repository.technology_repository import TechnologyRepository
from repository.project_technology_repository import ProjectTechnologyRepository
from repository.user_project_repository import UserProjectRepository
from service.project_service import ProjectService
from service.technology_service import TechnologyService
from controller.user_controller import user_service
from controller.client_controller import client_service
from controller.department_controller import department_service

technology_service = TechnologyService(TechnologyRepository())
project_service = ProjectService(ProjectRepository(), ProjectTechnologyRepository(), UserProjectRepository(),
                                 technology_service, user_service, client_service)

projects = Blueprint('projects', __name__)
__tech_path = '/projects/technologies'
__users_path = '/projects/users'
__tech_users_path = '/users/technologies'


@projects.route('/projects', methods=['GET'])
@auth_required_with_role([Role.administrator, Role.scrum_master])
def get_all_projects():
    project_id = request.args.get('projectid')
    if project_id is None:
        projects_list = []

        for project in project_service.getAllProjects():
            employees = [Mapper.get_instance().user_to_json(x) for x in project_service.getUsersForProject(project.id)]
            technologies = [Mapper.get_instance().technology_to_json(x) for x in project_service.getTechnologiesForProject(project.id)]
            client = Mapper.get_instance().client_to_json(client_service.getOne(project.client_id))
            projects_list.append(Mapper.get_instance().project_to_json(project, employees, technologies, client))

        return jsonify(projects_list)
    else:
        try:
            return Mapper.get_instance().project_to_json(project_service.getOneProject(project_id))
        except ValueError as err:
            return Response(str(err), 400)


@projects.route('/projects', methods=['POST'])
@auth_required_with_role([Role.administrator, Role.scrum_master])
def save_project():
    project = Mapper.get_instance().json_to_project(request.json)
    try:
        project_service.addProject(project)
    except ValueError as err:
        return Response(str(err), 400)
    return Mapper.get_instance().project_to_json(project)


@projects.route('/projects', methods=['PUT'])
@auth_required_with_role([Role.administrator, Role.scrum_master])
def update_project():
    project = Mapper.get_instance().json_to_project(request.json)
    try:
        project_service.updateProject(project)
    except ValueError as err:
        return Response(str(err), 400)
    return Mapper.get_instance().project_to_json(project)


@projects.route('/projects', methods=['DELETE'])
@auth_required_with_role([Role.administrator, Role.scrum_master])
def delete_project():
    project_id = request.args.get('projectid')
    try:
        project_service.removeProject(project_id)
    except ValueError as err:
        return Response(str(err), 400)
    return jsonify(success=True)


@projects.route(__tech_path, methods=['GET'])
@auth_required_with_role([Role.administrator, Role.scrum_master])
def get_technologies():
    project_id = request.args.get('projectid')
    tech_id = request.args.get('techid')
    if project_id is None and tech_id is None:
        return jsonify([Mapper.get_instance().technology_to_json(x) for x in technology_service.getAll()])

    if tech_id is None:
        try:
            return jsonify(
                [Mapper.get_instance().technology_to_json(x) for x in
                 project_service.getTechnologiesForProject(project_id)])
        except ValueError as err:
            return Response(str(err), 400)

    if project_id is None:
        try:
            return Mapper.get_instance().technology_to_json(technology_service.getOne(tech_id))
        except ValueError as err:
          return Response(str(err), 400)

    return jsonify(assigned=project_service.isTechAssignedToProject(project_id, tech_id))


# O tehnologie nu poate exista daca nu e asignata la minimum 1 proiect
# Daca nu exista deja, tehnologia e creata si adaugata
@projects.route(__tech_path, methods=['POST'])
@auth_required_with_role([Role.administrator, Role.scrum_master])
def assign_techs():
    project_id = request.args.get('projectid')
    techs = Mapper.get_instance().json_to_technologies(request.json)
    try:
        for tech in techs:
            project_service.assignTechToProject(project_id, tech)
        return jsonify(success=True)
    except ValueError as err:
        return Response(str(err), 400)


@projects.route(__tech_path, methods=['DELETE'])
@auth_required_with_role([Role.administrator, Role.scrum_master])
def unassign_tech():
    project_id = request.args.get('projectid')
    tech_id = request.args.get('techid')
    try:
        project_service.unassignTechFromProject(project_id, tech_id)
        return jsonify(success=True)
    except ValueError as err:
        return Response(str(err), 400)


@projects.route(__users_path, methods=['GET'])
@auth_required_with_role([Role.administrator, Role.scrum_master, Role.employee])
def get_users():
    project_id = request.args.get('projectid')
    user_id = request.args.get('userid')
    if project_id is not None and user_id is not None:
        return jsonify(assigned=project_service.isUserAssignedToProject(project_id, user_id))

    if project_id is not None:
        try:
            users = project_service.getUsersForProject(project_id)
            return jsonify(
                 [Mapper.get_instance().user_to_json(x, Mapper.get_instance().department_to_json(department_service.getOne(x.get_department_id()))) for x in users])
        except ValueError as err:
            return Response(str(err), 400)

    if user_id is not None:
        try:
            return jsonify([Mapper.get_instance().project_to_json(x) for x in project_service.getProjectsForUser(user_id)])
        except ValueError as err:
            return Response(str(err), 400)


@projects.route("/projects/userslist", methods=['GET'])
@auth_required_with_role([Role.administrator, Role.scrum_master])
def get_users_and_nr_of_projects():
    list = []
    for user in user_service.getAll():
        nrOfProjectsForCurrentUser = len(project_service.getProjectsForUser(user.get_id()))
        list.append([user,nrOfProjectsForCurrentUser])
    try:
        return jsonify([Mapper.get_instance().user_to_json(x[0],nrofprojects=x[1]) for x in list])
    except ValueError as err:
        return Response(str(err), 400)


@projects.route(__users_path, methods=['POST'])
@auth_required_with_role([Role.administrator, Role.scrum_master])
def assign_users():
    project_id = request.args.get('projectid')
    try:
        for user in request.json['users']:
            project_service.assignUserToProject(project_id, user['id'])
        return jsonify(success=True)
    except ValueError as err:
        return Response(str(err), 400)


@projects.route(__users_path, methods=['DELETE'])
@auth_required_with_role([Role.administrator, Role.scrum_master])
def unassign_user():
    project_id = request.args.get('projectid')
    user_id = request.args.get('userid')
    try:
        project_service.unassignUserFromProject(project_id, user_id)
        return jsonify(success=True)
    except ValueError as err:
        return Response(str(err), 400)


@projects.route(__tech_users_path, methods=['GET'])
@auth_required_with_role([Role.administrator, Role.scrum_master])
def get_users_by_technology():
    return jsonify(project_service.get_technologies_and_users_with_recommandation())


#TODO Change hardcoded route and enable auth
@projects.route('/tp', methods=['GET'])
#@auth_required_with_role([Role.administrator, Role.scrum_master])
def get_most_used_technologies():
    rez={}
    for i,el in enumerate(technology_service.getMostUsedTechnologies()):
        tech_json_with_nrproj=Mapper.get_instance().technology_to_json(el[0])
        tech_json_with_nrproj['nr_of_projects']=el[1]
        rez[i]=tech_json_with_nrproj
    return jsonify(rez)
