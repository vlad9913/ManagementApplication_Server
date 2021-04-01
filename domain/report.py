from controller import db


#  Reprezinta o nota (mark) pe care a primit-o un user (user_id), in cadrul unui anumit proiect (priject_id), pentru un
#    anumit skill (skill_id).
class Report(db.Model):
    __tablename__ = 'Reports'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))  # ID-ul userului caruia i s-a facut report-ul
    skill_id = db.Column(db.Integer, db.ForeignKey('Skills.id'))  # Skill-ul pentru care s-a facut report
    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id'))  # Proiectul in cadrul caruia s-a primit feedback
    mark = db.Column('mark', db.Integer)
    date = db.Column('date', db.DateTime)

    def __init__(self, id, user_id, skill_id, project_id, mark, date):
        self.id = id
        self.user_id = user_id
        self.skill_id = skill_id
        self.project_id = project_id
        self.mark = mark
        self.date = date

    def set_user_id(self, value):
        self.user_id = value

    def set_skill_id(self, value):
        self.skill_id = value

    def set_project_id(self, value):
        self.project_id = value

    def set_mark(self, value):
        self.mark = value

    def set_date(self, value):
        self.date = value

    def set_id(self, value):
        self.id = value

    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_skill_id(self):
        return self.skill_id

    def get_project_id(self):
        return self.project_id

    def get_mark(self):
        return self.mark

    def get_date(self):
        return self.date
