from flask import Flask
from app import views
from app import db


def create_app():
    app = Flask(__name__)
    app.register_blueprint(views.bp_ui)
    app.register_blueprint(views.bp_api)
    app.teardown_appcontext(db.close_db)
    return app
