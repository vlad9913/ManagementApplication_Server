from flask import Blueprint, Response
from flask import jsonify, request

from controller.helpers.authorize import auth_required_with_role
from controller.helpers.mapper import Mapper
from domain.enums.role import Role
from repository.report_repository import ReportRepository
from repository.report_session_repository import ReportSessionRepository
from repository.skill_repository import SkillRepository
from service.feedback_service import FeedbackService
from controller.project_controller import project_service

feedback_service = FeedbackService(ReportRepository(), ReportSessionRepository(), SkillRepository(), project_service)

feedback = Blueprint('feedback', __name__)
__base_path = '/feedback'
__report_sessions_path = __base_path + '/sessions'
__skills_path = __base_path + '/skills'


@feedback.route(__skills_path, methods=['GET'])
@auth_required_with_role([Role.administrator, Role.employee, Role.scrum_master])
def get_all_skills():
    return jsonify([Mapper.get_instance().skill_to_json(x) for x in feedback_service.getAllSkills()])


@feedback.route(__report_sessions_path, methods=['GET'])
@auth_required_with_role([Role.administrator, Role.employee, Role.scrum_master])
def get_report_sessions():
    user_id = request.args.get('userid')
    project_id = request.args.get('projectid')
    if user_id is None and project_id is None:
        return jsonify(
            [Mapper.get_instance().report_session_to_json(x, project_service.getOneProject(x.get_project_id())) for x in
             feedback_service.getAllReportSessions()])

    if user_id is not None:
        try:
            return jsonify(
                [Mapper.get_instance().report_session_to_json(x, project_service.getOneProject(x.get_project_id())) for
                 x in
                 feedback_service.getAllReportSessionsForUser(user_id)])
        except ValueError as err:
            return Response(str(err), 400)

    if project_id is not None:
        try:
            list = feedback_service.getAllReportSessionsForProject(project_id)
            for x in list:
                x['start_date'] = x['start_date'].strftime(Mapper.get_date_time_format())
                x['end_date'] = x['end_date'].strftime(Mapper.get_date_time_format())
            return jsonify(list)
        except ValueError as err:
            return Response(str(err), 400)


# Va deschide un report session pentru fiecare user membru al proiectului dat
@feedback.route(__report_sessions_path, methods=['POST'])
@auth_required_with_role([Role.administrator, Role.employee, Role.scrum_master])
def add_report_sessions():
    project_id = request.json['project_id']
    start_date = Mapper.get_instance().json_to_date_time(request.json['start_date'])
    end_date = Mapper.get_instance().json_to_date_time(request.json['end_date'])
    try:
        count = feedback_service.addReportSessions(project_id, start_date, end_date)
    except ValueError as err:
        return Response(str(err), 400)
    return jsonify(added=count)


# Va sterge doar report session-urile necompletate
@feedback.route(__report_sessions_path, methods=['DELETE'])
@auth_required_with_role([Role.administrator, Role.employee, Role.scrum_master])
def delete_report_sessions():
    project_id = request.json['project_id']
    start_date = Mapper.get_instance().json_to_date_time(request.json['start_date'])
    end_date = Mapper.get_instance().json_to_date_time(request.json['end_date'])
    try:
        count = feedback_service.removeReportSessions(project_id, start_date, end_date)
    except ValueError as err:
        return Response(str(err), 400)
    return jsonify(removed=count)


@feedback.route(__base_path, methods=['POST'])
@auth_required_with_role([Role.administrator, Role.employee, Role.scrum_master])
def add_reports():
    from datetime import datetime
    report_session_id = request.args.get('sessionid')
    try:
        count = feedback_service.addReports(report_session_id, Mapper.get_instance().json_to_reports(request.json),
                                            datetime.now())
    except ValueError as err:
        return Response(str(err), 400)
    return jsonify(added=count)
