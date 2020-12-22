from flask import Blueprint, render_template, request, redirect, abort, url_for
from paapas.pa.pa_db import get_from_db, add_to_db
from paapas.pa import options, input_types

bp_ui = Blueprint('ui', __name__, url_prefix='/ui')


@bp_ui.route('/')
def home():
    """
    Default route for personal assistant UI

    :return: rendered template of 'ui_home.html'
    """

    return render_template('pa/ui_home.html',
                           options=options,
                           reminders=get_from_db('reminder'),
                           todos=get_from_db('todo'))


@bp_ui.route('/add/<add_type>', methods=('GET', 'POST'))
def add(add_type):
    """
    Generic route to setup a template for adding items to the database

    This route provides a user interface for adding an arbitrary type from the list of options to the db.
    The template will be rendered at runtime with the title and fields corresponding to the type being added.
    This method handles both the 'GET' and 'POST' http requests, serving a html page for 'GET' and validating
    and processing the form for 'POST'

    :param add_type: the type to add, see 'options'
    :return: either a webpage if 'GET', or a redirect to 'ui.home' if 'POST'
    """

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