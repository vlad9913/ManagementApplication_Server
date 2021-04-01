class FeedbackService:
    def __init__(self, report_repo, report_session_repo, skills_repo, project_service):
        self.__report_repo = report_repo
        self.__report_session_repo = report_session_repo
        self.__skills_repo = skills_repo
        self.__project_service = project_service

    def getAllSkills(self):
        return self.__skills_repo.getAll()

    def getAllReportSessions(self):
        return self.__report_session_repo.getAll()

    def getAllReportSessionsForUser(self, userId):
        from controller.user_controller import user_service
        user_service.getOne(userId) # raises ValueError if user with userId does not exist
        return self.__report_session_repo.getAllForUser(userId)

    def getAllReportSessionsForProject(self, projectId):
        from controller.project_controller import project_service
        project_service.getOneProject(projectId) # raises ValueError if project with projectId does not exist

        rs = self.__report_session_repo.getAllForProject(projectId)

        dictionar = {}
        for x in rs:
            tup = (x.get_project_id(), x.get_start_date(), x.get_end_date())
            if tup not in dictionar:
                dictionar[tup] = (0, 1)
            else:
                dictionar[tup][1] += 1
            if x.get_was_completed() is True:
                dictionar[tup][0] += 1

        out = []
        for key in dictionar.keys():
            out.append({'projectId': key[0], 'start_date': key[1], 'end_date': key[2], 'completed': dictionar[key][0],
                        'total': dictionar[key][1]})
        return out

    def addReportSessions(self, projectId, startDate, endDate):
        from domain.report_session import ReportSession

        if startDate >= endDate:
            raise ValueError("Invalid start/end dates")

        count = 0
        for user in self.__project_service.getUsersForProject(projectId):
            # raises ValueError if project with given ID
            #  does not exist
            self.__report_session_repo.add(ReportSession(None, projectId, user.get_id(), startDate, endDate, False))
            count += 1
        return count

    def removeReportSessions(self, projectId, startDate, endDate):

        from controller.project_controller import project_service
        project_service.getOneProject(projectId)  # raises ValueError if project with projectId does not exist

        sessions = self.__report_session_repo.getAllForProject(projectId)
        count = 0
        for x in sessions:
            if x.get_start_date() == startDate and x.get_end_date() == endDate and x.get_was_completed() is False:
                self.__report_session_repo.remove(x)
                count += 1
        return count

    def addReports(self, sessionId, reports, currentTime):
        session = self.__report_session_repo.getOne(sessionId)
        if session is None:
            raise ValueError("The given report session does not exist")

        if session.get_was_completed() is True:
            raise ValueError("The report session was already completed")

        if currentTime < session.get_start_date():
            raise ValueError("The report session has not yet started")

        if currentTime > session.get_end_date():
            raise ValueError("The report session has ended")

        count = 0
        check = []
        for report in reports:
            if report.get_user_id() == session.get_user_id():  # Nu isi poate da feedback singur
                continue

            if not self.__project_service.isUserAssignedToProject(report.get_user_id(), session.get_project_id()):
                continue

            if self.__skills_repo.getOne(report.get_skill_id()) is None:
                continue

            tup = (report.get_user_id(), report.get_skill_id())
            if tup in check:
                continue

            check.append(tup)

            report.set_id(None)  # Autoincrement
            report.set_date(currentTime)
            self.__report_repo.add(report)
            count += 1

        session.set_was_completed(True)
        self.__report_session_repo.update(session)
        return count

    # Deletes all reports report sessions, regardless of completed or not. Used when deleting projects
    def forceDeleteFeedbackDataForProject(self, projectId):
        sessions = self.__report_session_repo.getAllForProject(projectId)
        for x in sessions:
            self.__report_session_repo.remove(x)

        reports = self.__report_repo.getAllForProject(projectId)
        for x in reports:
            self.__report_repo.remove(x)

    # Used when deleting users
    def forceDeleteFeedbackDataForUser(self, userId):
        sessions = self.__report_session_repo.getAllForUser(userId)
        for x in sessions:
            self.__report_session_repo.remove(x)

        reports = self.__report_repo.getAllForUser(userId)
        for x in reports:
            self.__report_repo.remove(x)

    # Apelata doar manual
    def populateSkills(self):
        from domain.skill import Skill
        self.__skills_repo.add(Skill(1, 'Completes the work thoroughly and with care'))
        self.__skills_repo.add(Skill(2, 'Understands the assigned role and responsibilities'))
        self.__skills_repo.add(Skill(3, 'Delivers consistently to agreed time-frames and specifications'))
        self.__skills_repo.add(Skill(4, 'Communicates in a professional and responsive manner'))
        self.__skills_repo.add(Skill(5, 'Is motivated by the work he/she is doing'))
        self.__skills_repo.add(Skill(6, 'Is adaptable to new types of assignments'))
        self.__skills_repo.add(Skill(7, 'How would you rate overall performance?'))
        self.__skills_repo.add(Skill(8, 'How would you rate employee Work From Home(WFH) performance?'))
