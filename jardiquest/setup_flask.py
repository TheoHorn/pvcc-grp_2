from flask import Flask
from flask_login import LoginManager

from jardiquest import controller, model
from jardiquest.model.database.entity.user import User
from jardiquest.setup_sql import db, database_path


# create the flask app (useful to be separate from the app.py
# to be used in the test and to put all the code in the jardiquest folder
def create_app():
    db_path = 'sqlite://' + database_path
    # config the app to make app.py the start point but the actual program is one directory lower
    flask_serv_intern = Flask(__name__,
                              static_folder="static",
                              template_folder='view')

    flask_serv_intern.config['SQLALCHEMY_DATABASE_URI'] = db_path
    flask_serv_intern.config['SECRET_KEY'] = '=xyb3y=2+z-kd!3rit)hfrg0j!e!oggyny0$5bliwlb8v76j'
    flask_serv_intern.register_blueprint(controller.app)
    db.init_app(flask_serv_intern)

    with flask_serv_intern.app_context():
        db.create_all()

    # login handling
    login_manager = LoginManager()
    login_manager.login_view = 'controller.login'
    login_manager.init_app(flask_serv_intern)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # all operation of closing ressources like database
    @flask_serv_intern.teardown_appcontext
    def close_ressource(exception):
        model.close_connection(exception)

    return flask_serv_intern
