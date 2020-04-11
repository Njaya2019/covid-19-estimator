from flask import Flask
from errorhandlers import page_is_forbidden, page_not_found, page_was_deleted,\
                          httpmethod_not_allowed, server_error
from estimator_blueprint import estimate_blueprint
from configurations import ProductionConfig


def create_app(enviroment, configfile=None):

    # Creates an instance app of the flask class

    app = Flask(__name__, instance_relative_config=True)

    # Loads configuration from the configurations class
    # And updates config dictinary.

    app.config.from_object(enviroment)

    # Loads a key value pair from a configfile to
    # override some of the configuration from the
    # main configurations.

    app.config.from_pyfile(configfile, silent=True)

    # Registers blueprints

    app.register_blueprint(estimate_blueprint)

    # register application exceptions

    app.register_error_handler(404, page_not_found)

    app.register_error_handler(403, page_is_forbidden)

    app.register_error_handler(410, page_was_deleted)

    app.register_error_handler(500, server_error)

    app.register_error_handler(405, httpmethod_not_allowed)

    return app

# Runs the function and captures the return in app variable

app = create_app(ProductionConfig, 'config.py')

# Runs the app

if __name__ == "__main__":

    app.run()
