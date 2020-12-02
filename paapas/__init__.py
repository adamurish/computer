from flask import Flask
from paapas import db, home
from paapas.pa import api, ui


def create_app():
    app = Flask(__name__)
    app.register_blueprint(pa.ui.bp_ui)
    app.register_blueprint(pa.api.bp_api)
    app.register_blueprint(home.bp_home)
    app.teardown_appcontext(db.close_db)

    return app
