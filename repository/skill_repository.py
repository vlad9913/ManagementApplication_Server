class SkillRepository:
    def getAll(self):
        from domain.skill import Skill

        skills = Skill.query.all()
        return skills

    def getOne(self, skillId):
        from domain.skill import Skill

        skill = Skill.query.get(skillId)
        return skill

    def add(self, skill):
        from controller import db
        db.session.add(skill)
        db.session.commit()
        return skill

    def remove(self, skill):
        from controller import db
        db.session.delete(skill)
        db.session.commit()
