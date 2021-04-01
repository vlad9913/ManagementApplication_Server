class ReportSessionRepository:
    def getAll(self):
        from domain.report_session import ReportSession
        return ReportSession.query.all()

    def getAllForUser(self, userId):
        from domain.report_session import ReportSession
        return ReportSession.query.filter(ReportSession.user_id == userId).all()

    def getAllForProject(self, projectId):
        from domain.report_session import ReportSession
        return ReportSession.query.filter(ReportSession.project_id == projectId).all()

    def getOne(self, reportSessionId):
        from domain.report_session import ReportSession
        return ReportSession.query.get(reportSessionId)

    def add(self, reportSession):
        from controller import db
        db.session.add(reportSession)
        db.session.commit()
        return reportSession

    def remove(self, reportSession):
        from controller import db
        db.session.delete(reportSession)
        db.session.commit()

    def update(self, reportSession):
        from controller import db
        from domain.report_session import ReportSession

        reportFound = ReportSession.query.get(reportSession.get_id())
        reportFound.set_user_id(reportSession.get_user_id())
        reportFound.set_project_id(reportSession.get_project_id())
        reportFound.set_start_date(reportSession.get_start_date())
        reportFound.set_end_date(reportSession.get_end_date())
        reportFound.set_was_completed(reportSession.get_was_completed())
        db.session.commit()
        return reportSession
