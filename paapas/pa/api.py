from flask import Blueprint, render_template, request, redirect, abort, url_for
from paapas.pa.pa_db import add_to_db
from paapas.pa import options

bp_api = Blueprint('api', __name__, url_prefix='/api')


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
