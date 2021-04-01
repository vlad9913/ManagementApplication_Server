class ClientService:
    def __init__(self, __repo):
        self.__repo = __repo

    def add(self, client):
        clientfound = self.__repo.getOne(client.get_id())
        if clientfound is not None:
            raise ValueError("A client with the given ID already exists.")
        return self.__repo.add(client)

    def getAll(self):
        clients = self.__repo.getAll()
        return clients

    def getOne(self, id):
        client = self.__repo.getOne(id)
        if client is None:
            raise ValueError("The client with the given ID does not exist.")
        return client

    def remove(self, id):
        client = self.__repo.getOne(id)
        if client is None:
            raise ValueError("The client with the given ID does not exist.")

        from controller.project_controller import project_service
        for proj in project_service.getAllProjects():
            if proj.get_client_id() == client.get_id():
                raise ValueError("Cannot delete client with assigned projects.")

        self.__repo.remove(client)

    def update(self, client):
        clientfound = self.__repo.getOne(client.get_id())
        if clientfound is None:
            raise ValueError("The client with the given ID does not exist.")

        self.__repo.update(client)
        return client
