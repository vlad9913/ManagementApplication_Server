

class UserRepository:
    def findByEmail(self,email):
        from domain.user import User
        return User.query.filter_by(email=email).first()

    def getAll(self):
        from domain.user import User

        users = User.query.all()
        return users

    def getOne(self,id):
        from domain.user import User

        user = User.query.get(id)
        return user

    def add(self,user):
        from controller import db
        db.session.add(user)
        db.session.commit()
        return user

    def remove(self,user):
        from controller import db
        db.session.delete(user)
        db.session.commit()

    def update(self,user):
        from controller import db
        from domain.user import User

        userfound = User.query.get(user.get_id())
        userfound.set_name(user.get_name())
        userfound.set_email(user.get_email())
        userfound.set_role(user.get_role())
        userfound.set_seniority_level(user.get_seniority_level())
        userfound.set_department_id(user.get_department_id())
        db.session.commit()
        return user