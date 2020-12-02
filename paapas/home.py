from flask import Blueprint, redirect, url_for

bp_home = Blueprint('home', __name__)


@bp_home.route('/')
def index():
    return redirect(url_for('ui.home'))
