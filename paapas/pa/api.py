import json
from flask import Blueprint, render_template, request, redirect, abort, url_for
from paapas.pa.pa_db import add_to_db, get_from_db_raw
from paapas.pa import options
from bson import json_util

bp_api = Blueprint('api', __name__, url_prefix='/api')


def check_request():
    """
    Verify that the current request conforms to standard json structure

    Creates a status dict with at least a 'success' attribute
    This status will also have a 'reason' attribute if the request is malformed

    :return: the status dict
    """

    status = {
        'success': True,
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
    """
    API route to add content to the database

    This method verifies that the request is properly formed, see 'check_request()'

    The item to add should be something from the 'options' dict.
    It will be added to the collection matching the 'type' attribute in the request.

    :return: status dict, see 'check_request()' for more info
    """

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


@bp_api.route('/get', methods=('POST',))
def api_get():
    """
    API route to get content stored in the database

    This method verifies that the request is properly formed, see 'check_request()'

    The json request must contain a 'type' attribute, one of the types contained in 'options.'
    The method will return all items in the database collection matching that type,
    stored in the status dict under 'content'

    :return:  status dict, see 'check_request()' for more info
    """

    status = check_request()
    if not status['success']:
        return status
    status['content'] = json.loads(json_util.dumps(get_from_db_raw(request.json['type'])))
    return status
