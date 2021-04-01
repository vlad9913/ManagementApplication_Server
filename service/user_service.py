import secrets
import string
from datetime import datetime, timedelta

import jwt
from werkzeug.security import check_password_hash
import smtplib, ssl
from email.message import EmailMessage

from domain.enums.role import Role


class UserService:
    def __init__(self, __repo):
        self.__repo = __repo

    def matchUserPassword(self, email, password):
        addedUser = self.__repo.findByEmail(email)
        if not addedUser or check_password_hash(addedUser.get_password(), password) is False:
            return None  # if the user doesn't exist or password is wrong, return null
        return addedUser

    def add(self, user):
        userfound = self.__repo.getOne(user.get_id())
        if userfound is not None:
            raise ValueError("A user with the given ID already exists.")
        return self.__repo.add(user)

    def getAll(self):
        users = self.__repo.getAll()
        return users

    def getOne(self, id):
        user = self.__repo.getOne(id)
        if user is None:
            raise ValueError("The user with the given ID does not exist.")
        return user

    def remove(self, id):
        user = self.__repo.getOne(id)
        if user is None:
            raise ValueError("The user with the given ID does not exist.")
        from controller.project_controller import project_service
        for project in project_service.getProjectsForUser(user.get_id()):
            project_service.unassignUserFromProject(project.get_id(), user.get_id())

        from controller.feedback_controller import feedback_service
        feedback_service.forceDeleteFeedbackDataForUser(user.get_id())
        
        self.__repo.remove(user)

    def update(self, user):
        userfound = self.__repo.getOne(user.get_id())
        if userfound is None:
            raise ValueError("The user with the given ID does not exist.")

        self.__repo.update(user)

        return user

    def __get_generated_password(self):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(20))

    def send_password_email(self, user):
        gmail_user = 'colectivgrupa3@gmail.com'  # trebuie introduse
        gmail_password = 'colectiv123!!!'  # cele corecte si adevarate ! ! !

        user.set_password(self.__get_generated_password())

        msg = EmailMessage()
        msg['Subject'] = 'Your password at our company.'
        msg['From'] = gmail_user
        msg['To'] = user.get_email()
        # msg['To'] = gmail_user  # trimit mail-ul pe acelasi cont pentru test
        msg.set_content('Hello, here is your password: ' + user.get_password())

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
        except smtplib.SMTPException:
            raise ValueError("Could not send registration email.")

    def generate_token(self, user_id):
        user = self.__repo.getOne(user_id)
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1, seconds=0),
            'public_id': user_id,
            'role': user.role
        }

        token = jwt.encode(payload, 'super-secret-key', algorithm='HS256')
        return token.decode("utf-8")
