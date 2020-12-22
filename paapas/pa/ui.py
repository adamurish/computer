from flask import Blueprint, render_template, request, redirect, abort, url_for
from paapas.db import get_db
from paapas.pa.pa_db import get_from_db, add_to_db
from paapas.pa import options, input_types

bp_ui = Blueprint('ui', __name__, url_prefix='/ui')


@bp_ui.route('/')
def home():
    return render_template('pa/ui_home.html',
                           options=options,
                           reminders=get_from_db('reminder'),
                           todos=get_from_db('todo'))


@bp_ui.route('/add/<add_type>', methods=('GET', 'POST'))
def add(add_type):
    add_type = str.lower(add_type)
    if options[add_type] is None:
        abort(404)
    if request.method == 'POST':
        add_to_db(add_type, dict(request.form))
        return redirect(url_for('ui.home'))
    inputs = []
    for i in range(len(options[add_type])):
        inputs.append((options[add_type][i], input_types[add_type][i], str.capitalize(options[add_type][i])))
    return render_template('pa/ui_add.html', type=str.capitalize(add_type), inputs=inputs)