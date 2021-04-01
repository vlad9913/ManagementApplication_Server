from controller import db


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String)
    email = db.Column('email', db.String)
    password = db.Column('password', db.String)
    role = db.Column('role', db.SmallInteger)
    seniority_level = db.Column('seniority_level', db.SmallInteger)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id'))

    def __init__(self, id, name, email, password, role, seniority_level, department_id):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.seniority_level = seniority_level
        self.department_id = department_id

    def set_id(self, value):
        self.id = value

    def set_name(self, value):
        self.name = value

    def set_email(self, value):
        self.email = value

    def set_password(self, value):
        self.password = value

    def set_role(self, value):
        self.role = value

    def set_seniority_level(self, value):
        self.seniority_level = value

    def set_department_id(self, value):
        self.department_id = value

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_role(self):
        return self.role

    def get_seniority_level(self):
        return self.seniority_level

    def get_department_id(self):
        return self.department_id
