class DepartmentService:
    def __init__(self, __repo):
        self.__repo = __repo

    def add(self, department):
        departmentfound = self.__repo.getOne(department.get_id())
        if departmentfound is not None:
            raise ValueError("A department with the given ID already exists.")
        return self.__repo.add(department)

    def getAll(self):
        departments = self.__repo.getAll()
        return departments

    def getOne(self, id):
        department = self.__repo.getOne(id)
        if department is None:
            raise ValueError("The department with the given ID does not exist.")
        return department

    def remove(self, id):
        department = self.__repo.getOne(id)
        if department is None:
            raise ValueError("The department with the given ID does not exist.")

        from controller.user_controller import user_service
        for user in user_service.getAll():
            if user.get_department_id() == department.get_id():
                raise ValueError("Cannot delelte department with assigned users.")

        self.__repo.remove(department)

    def update(self, department):
        departmentfound = self.__repo.getOne(department.get_id())
        if departmentfound is None:
            raise ValueError("The department with the given ID does not exist.")
        self.__repo.update(department)
        return department
