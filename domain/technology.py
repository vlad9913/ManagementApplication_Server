from controller import db


class Technology(db.Model):
    __tablename__ = "Technologies"
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def set_id(self, value):
        self.id = value

    def set_name(self, value):
        self.name = value

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name
