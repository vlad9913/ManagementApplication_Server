class DepartmentRepository:

    def getAll(self):
        from domain.department import Department

        departments = Department.query.all()
        return departments

    def getOne(self,id):
        from domain.department import Department

        department = Department.query.get(id)
        return department

    def add(self,department):
        from controller import db
        db.session.add(department)
        db.session.commit()
        return department

    def remove(self,department):
        from controller import db
        db.session.delete(department)
        db.session.commit()

    def update(self,department):
        from controller import db
        from domain.department import Department

        departmentfound = Department.query.get(department.get_id())
        departmentfound.set_name(department.get_name())
        departmentfound.set_description(department.get_description())
        db.session.commit()
        return department