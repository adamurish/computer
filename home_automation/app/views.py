from flask import Blueprint, render_template, request, redirect, abort, url_for
from app.db import get_db

bp_ui = Blueprint('ui', __name__)
bp_api = Blueprint('api', __name__, url_prefix='/api')
options = {
    'alarm': ['date', 'time'],
    'reminder': ['date', 'time', 'text'],
    'todo': ['date', 'time', 'text', 'priority'],
}

input_types = {
    'alarm': ['date', 'time'],
    'reminder': ['date', 'time', 'text'],
    'todo': ['date', 'time', 'text', 'number'],
}


def add_to_db(collection, content):
    db = get_db().get_database('home_automation')
    db.get_collection(collection).insert_one(content)


def get_from_db(collection, filter=None):
    db = get_db().get_database('home_automation')
    ret = []
    for entry in db.get_collection(collection).find(filter):
        entry['labels'] = {}
        for field in options[collection]:
            entry['labels'][field] = str.capitalize(field)
        ret.append(entry)
    return ret


@bp_ui.route('/')
def home():
    print(get_from_db('reminder'))
    return render_template('ui_home.html', options=options, reminders=get_from_db('reminder'), todos=get_from_db('todo'))


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
    return render_template('ui_add.html', type=str.capitalize(add_type), inputs=inputs)


@bp_api.route('/add', methods=('POST',))
def api_add():
    status = {
        'success': True
    }
    if not request.is_json:
        status['success'] = False
        status['reason'] = 'Not json'
        return status
    if 'type' not in request.json:
        status['success'] = False
        status['reason'] = 'Missing type'
        return status
    if options[request.json['type']] is None:
        status['success'] = False
        status['reason'] = "Bad type"
    content = {}
    for option in options[request.json['type']]:
        if option not in request.json:
            status['success'] = False
            status['reason'] = 'Missing ' + option
            return status
        content[option] = request.json[option]
    add_to_db(request.json['type'], content)
    return status
