from flask import Flask
from jardiquest import controller, model


# create the flask app (useful to be separate from the app.py
# to be used in the test and to put all the code in the jardiquest folder
def create_app():
    # config the app to make app.py the start point but the actual program is one directory lower
    flask_serv_intern = Flask(__name__,
                              static_folder="static",
                              template_folder='view')

    # allow the link to the controller part
    flask_serv_intern.register_blueprint(controller.app)

    # all operation of closing ressources like database
    @flask_serv_intern.teardown_appcontext
    def close_ressource(exception):
        model.close_connection(exception)

    return flask_serv_intern
