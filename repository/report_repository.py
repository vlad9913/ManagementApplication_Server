class ReportRepository:
    def getAll(self):
        from domain.report import Report
        return Report.query.all()

    def getAllForUser(self, userId):
        from domain.report import Report
        return Report.query.filter(Report.user_id == userId).all()

    def getAllForProject(self, projectId):
        from domain.report import Report
        return Report.query.filter(Report.project_id == projectId).all()

    def getOne(self, reportId):
        from domain.report import Report
        return Report.query.get(reportId)

    def add(self, report):
        from controller import db
        db.session.add(report)
        db.session.commit()
        return report

    def remove(self, report):
        from controller import db
        db.session.delete(report)
        db.session.commit()

    def update(self, report):
        from controller import db
        from domain.report import Report

        reportFound = Report.query.get(report.get_id())
        reportFound.set_user_id(report.get_user_id())
        reportFound.set_skill_id(report.get_skill_id())
        reportFound.set_project_id(report.get_project_id())
        reportFound.set_mark(report.get_mark())
        reportFound.set_date(report.get_date())
        db.session.commit()
        return report
