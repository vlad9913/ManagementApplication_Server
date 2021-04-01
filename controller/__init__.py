from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from controller import user_controller
from controller import client_controller
from controller import department_controller
from controller import project_controller
from controller import feedback_controller

app = Flask(__name__)
app.register_blueprint(user_controller.auth)
app.register_blueprint(department_controller.deps)
app.register_blueprint(client_controller.clients)
app.register_blueprint(user_controller.users)
app.register_blueprint(project_controller.projects)
app.register_blueprint(feedback_controller.feedback)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = '123abc7891337'
app.config.from_object('database.database_config.Config')
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()
    # TODO
    '''
    -- BUG [Database] Deleting first time an user or project raise an internal server error
    -- Am incercat sa trimit un query pe fiecare tabel cand pornesc aplicatia, sa le incarce in memorie fortat pe toate
    -- Poate merge daca se intampla mai tarziu, nu chiar la lansare...
    
    user_controller.user_service.getAll()
    client_controller.client_service.getAll()
    department_controller.department_service.getAll()
    project_controller.project_service.getAll()
    '''
