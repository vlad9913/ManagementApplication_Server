import json

from flask import Blueprint, Response
from flask import jsonify, request

from controller.helpers.authorize import auth_required_with_role
from controller.helpers.mapper import Mapper
from domain.enums.role import Role
from repository.department_repository import DepartmentRepository
from repository.user_repository import UserRepository
from service.department_service import DepartmentService
from service.user_service import UserService
from werkzeug.security import generate_password_hash
user_repo = UserRepository()
user_service = UserService(user_repo)


users = Blueprint('users',__name__)
auth = Blueprint('auth', __name__)

userRepo = UserRepository()
userService = UserService(userRepo)
department_repo = DepartmentRepository()
department_service = DepartmentService(department_repo)

@auth.route('/login', methods=['POST'])
def login_post():
    user = userService.matchUserPassword(request.json['email'], request.json['password'])
    if user is None:
        return json.dumps(user)

    jsonUser = Mapper.get_instance().user_to_json(user)
    jsonUser['jwtToken'] = userService.generate_token(user.id)
    return jsonify(jsonUser)


@users.route('/users', methods=['GET'])
@auth_required_with_role([Role.administrator, Role.hr])
def get_users():
    user_id = request.args.get('userid')
    if user_id is None:
        # get all users
        users = []
        for user in user_service.getAll():
            department = Mapper.get_instance().department_to_json(department_service.getOne(user.department_id))
            users.append(Mapper.get_instance().user_to_json(user, department))
        return jsonify(users)
    else:
        # get one user
        try:
            user = user_service.getOne(user_id)
            return Mapper.get_instance().user_to_json(user)
        except ValueError as err:
            return Response(str(err), 400)


@users.route('/users', methods=['POST'])
@auth_required_with_role([Role.administrator, Role.hr])
def save_user():
    user = Mapper.get_instance().json_to_user(request.json)
    user.set_id(None)
    try:
        user_service.send_password_email(user) # old, plain text password is used to send it as an email to the user
        user.set_password(generate_password_hash(user.get_password())) # method : "pbkdf2:sha256"
        user_service.add(user)
        department = Mapper.get_instance().department_to_json(department_service.getOne(user.department_id))
    except ValueError as err:
        return Response(str(err), 400)
    return Mapper.get_instance().user_to_json(user, department)


@users.route('/users', methods=['PUT'])
@auth_required_with_role([Role.administrator, Role.hr])
def update_user():
    user = Mapper.get_instance().json_to_user(request.json)
    try:
        user_service.update(user)
        department = Mapper.get_instance().department_to_json(department_service.getOne(user.department_id))
    except ValueError as err:
        return Response(str(err), 400)
    return Mapper.get_instance().user_to_json(user, department)


@users.route('/users', methods=['DELETE'])
@auth_required_with_role([Role.administrator, Role.hr])
def delete_users():
    user_id = request.args.get('userid')
    try:
        user_service.remove(user_id)
    except ValueError as err:
        return Response(str(err), 400)
    return jsonify(success=True)