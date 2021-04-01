
class ClientRepository:

    def getAll(self):
        from domain.client import Client

        clients = Client.query.all()
        return clients

    def getOne(self,id):
        from domain.client import Client

        client = Client.query.get(id)
        return client

    def add(self,client):
        from controller import db
        db.session.add(client)
        db.session.commit()
        return client

    def remove(self,client):
        from controller import db
        db.session.delete(client)
        db.session.commit()

    def update(self,client):
        from controller import db
        from domain.client import Client

        clientfound = Client.query.get(client.get_id())
        clientfound.set_name(client.get_name())
        clientfound.set_description(client.get_description())
        db.session.commit()
        return client