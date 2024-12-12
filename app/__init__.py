from flask import Flask
from .blaze import BlazeSql
from .utils import get_files_list

def create_app():
    app = Flask(__name__)

    # Your routes and logic will go here
    from . import routes
    app.register_blueprint(routes.bp)

    return app
