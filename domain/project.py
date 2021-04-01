from sqlalchemy.orm import relationship

from controller import db


class Project(db.Model):
    __tablename__ = 'Projects'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String)
    description = db.Column('description', db.String)
    start_date = db.Column('start_date', db.Date)
    end_date = db.Column('end_date', db.Date)
    deadline_date = db.Column('deadline_date', db.Date)
    client_id = db.Column(db.Integer, db.ForeignKey("Clients.id"))

    def __init__(self, id, name, description, start_date, end_date, deadline_date, client_id):
        self.id = id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.deadline_date = deadline_date
        self.client_id = client_id

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

    def get_client_id(self):
        return self.client_id

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_deadline_date(self):
        return self.deadline_date

    def set_client_id(self, value):
        self.client_id = value

    def set_start_date(self, value):
        self.start_date = value

    def set_end_date(self, value):
        self.end_date = value

    def set_deadline_date(self, value):
        self.deadline_date = value

    def set_id(self, value):
        self.id = value

    def set_name(self, value):
        self.name = value

    def set_description(self, value):
        self.description = value
