from flask import Blueprint, Response
from flask import jsonify, request

from controller.helpers.authorize import auth_required_with_role
from controller.helpers.mapper import Mapper
from domain.enums.role import Role
from repository.department_repository import DepartmentRepository
from service.department_service import DepartmentService


department_repo = DepartmentRepository()
department_service = DepartmentService(department_repo)

deps = Blueprint('deps',__name__)


@deps.route('/departments', methods=['GET'])
@auth_required_with_role([Role.administrator, Role.hr])
def get_departments():
    department_id = request.args.get('departmentid')
    if department_id is None:
        # get all departments
        return jsonify(
            [Mapper.get_instance().department_to_json(department) for department in department_service.getAll()])
    else:
        # get one client
        try:
            department = department_service.getOne(department_id)
        except ValueError as err:
            return Response(str(err), 400)
        return Mapper.get_instance().client_to_json(department)


@deps.route('/departments', methods=['POST'])
@auth_required_with_role([Role.administrator, Role.hr])
def save_department():
    department = Mapper.get_instance().json_to_department(request.json)
    try:
        department_service.add(department)
    except ValueError as err:
        return Response(str(err), 400)
    return Mapper.get_instance().department_to_json(department)


@deps.route('/departments', methods=['PUT'])
@auth_required_with_role([Role.administrator, Role.hr])
def update_department():
    department = Mapper.get_instance().json_to_department(request.json)
    try:
        department_service.update(department)
    except ValueError as err:
        return Response(str(err), 400)
    return Mapper.get_instance().department_to_json(department)


@deps.route('/departments', methods=['DELETE'])
@auth_required_with_role([Role.administrator, Role.hr])
def delete_departments():
    department_id = request.args.get('departmentid')
    try:
        department_service.remove(department_id)
    except ValueError as err:
        return Response(str(err), 400)
    return jsonify(success=True)
