from database.database_config import Config
from flask_sqlalchemy import SQLAlchemy

from domain.skill import Skill
from domain.client import Client
from domain.technology import Technology
from domain.department import Department
from domain.user import User
from domain.project import Project
from domain.report_session import ReportSession
from domain.report import Report
from domain.project_technology import Project_Technology
from domain.user_project import User_Project


def run():
    from controller import db
    db.create_all()


run()
