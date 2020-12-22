from flask import Blueprint, render_template, request, redirect, abort, url_for
from paapas.pa.pa_db import add_to_db, get_from_db
from paapas.pa import options

bp_api = Blueprint('api', __name__, url_prefix='/api')


def check_request():
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
    return status


@bp_api.route('/add', methods=('POST',))
def api_add():
    status = check_request()
    if not status['success']:
        return status
    content = {}
    for option in options[request.json['type']]:
        if option not in request.json:
            status['success'] = False
            status['reason'] = 'Missing ' + option
            return status
        content[option] = request.json[option]
    add_to_db(request.json['type'], content)
    return status


@bp_api.route('/get')
def api_get():
    status = check_request()
    if not status['success']:
        return status
    status['content'] = get_from_db(request.json['type'])
    return status
