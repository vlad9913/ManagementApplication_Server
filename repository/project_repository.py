class ProjectRepository:
    def getAll(self):
        from domain.project import Project

        projects = Project.query.all()
        return projects

    def getOne(self, id):
        from domain.project import Project

        project = Project.query.get(id)
        return project

    def add(self, project):
        from controller import db
        db.session.add(project)
        db.session.commit()
        return project

    def remove(self, project):
        from controller import db
        db.session.delete(project)
        db.session.commit()

    def update(self, project):
        from controller import db
        from domain.project import Project

        projectFound = Project.query.get(project.get_id())
        projectFound.set_name(project.get_name())
        projectFound.set_description(project.get_description())
        projectFound.set_start_date(project.get_start_date())
        projectFound.set_end_date(project.get_end_date())
        projectFound.set_deadline_date(project.get_deadline_date())
        projectFound.set_client_id(project.get_client_id())
        db.session.commit()
        return project
