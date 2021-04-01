class UserProjectRepository:
    def getAll(self):
        from domain.user_project import User_Project

        up = User_Project.query.all()
        return up

    def getOne(self, userId, projectId):
        from domain.user_project import User_Project

        pt = User_Project.query.get((userId, projectId))
        return pt

    def getAllForProject(self, projectId):
        from domain.user_project import User_Project

        pt = User_Project.query.filter(User_Project.project_id == projectId).all()
        return pt

    def getAllForUser(self, userId):
        from domain.user_project import User_Project

        pt = User_Project.query.filter(User_Project.user_id == userId).all()
        return pt

    def add(self, user_project):
        from controller import db
        db.session.add(user_project)
        db.session.commit()
        return user_project

    def remove(self, user_project):
        from controller import db
        db.session.delete(user_project)
        db.session.commit()
