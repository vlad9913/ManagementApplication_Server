from controller import db


class Department(db.Model):
    __tablename__ = 'Departments'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String)
    description = db.Column('description', db.String)

    def __init__(self,id,name,description):
        self.id = id
        self.name = name
        self.description = description

    def set_id(self, value):
        self.id = value

    def set_name(self, value):
        self.name = value

    def set_description(self,value):
        self.description = value

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description
