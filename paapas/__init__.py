from flask import Flask
from paapas import db, home
from paapas.pa import api, ui
from paapas.big_data import data


def create_app():
    app = Flask('paapas')
    app.register_blueprint(pa.ui.bp_ui)
    app.register_blueprint(pa.api.bp_api)
    app.register_blueprint(big_data.data.bp_data)
    app.register_blueprint(home.bp_home)
    app.teardown_appcontext(db.close_db)

    return app
