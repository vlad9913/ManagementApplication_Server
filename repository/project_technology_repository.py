class ProjectTechnologyRepository:
    def getAll(self):
        from domain.project_technology import Project_Technology

        pt = Project_Technology.query.all()
        return pt

    def getOne(self, projectId, techId):
        from domain.project_technology import Project_Technology

        pt = Project_Technology.query.get((projectId, techId))
        return pt

    def getAllForProject(self, projectId):
        from domain.project_technology import Project_Technology

        pt = Project_Technology.query.filter(Project_Technology.project_id == projectId).all()
        return pt

    def getAllForTechnology(self, techId):
        from domain.project_technology import Project_Technology

        pt = Project_Technology.query.filter(Project_Technology.technology_id == techId).all()
        return pt

    def add(self, project_tech):
        from controller import db
        db.session.add(project_tech)
        db.session.commit()
        return project_tech

    def remove(self, project_tech):
        from controller import db
        db.session.delete(project_tech)
        db.session.commit()
