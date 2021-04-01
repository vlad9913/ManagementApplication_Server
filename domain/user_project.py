from controller import db


class User_Project(db.Model):
    __tablename__ = 'User_Project'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id'), primary_key=True)

    def __init__(self, user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id

    def get_user_id(self):
        return self.user_id

    def get_project_id(self):
        return self.project_id

    def set_user_id(self, value):
        self.user_id = value

    def set_project_id(self, value):
        self.project_id = value
