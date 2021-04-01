class TechnologyRepository:
    def getAll(self):
        from domain.technology import Technology

        techs = Technology.query.all()
        return techs

    def getOne(self, id):
        from domain.technology import Technology

        tech = Technology.query.get(id)
        return tech

    def add(self, tech):
        from controller import db
        db.session.add(tech)
        db.session.commit()
        return tech

    def remove(self, tech):
        from controller import db
        db.session.delete(tech)
        db.session.commit()

    def update(self, tech):
        from controller import db
        from domain.technology import Technology

        techFound = Technology.query.get(tech.get_id())
        techFound.set_name(tech.get_name())
        db.session.commit()
        return tech

    def getMostUsedTechnologies(self):
        #from controller import db
        from sqlalchemy import func

        from domain.project_technology import Project_Technology
        from domain.technology import Technology, db
        rez=db.session.query(Technology,func.count(Project_Technology.technology_id))\
            .select_from(Project_Technology)\
            .filter(Technology.id == Project_Technology.technology_id)\
            .group_by(Technology)\
            .all()
        maxi=max(el[1] for el in rez)
        rez=[el for el in rez if el[1]==maxi]
        return rez