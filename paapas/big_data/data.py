from flask import Blueprint, request
from paapas import db
from paapas.big_data import data_types
from datetime import datetime

bp_data = Blueprint('data', __name__, url_prefix='/data')


@bp_data.route('/post', methods=('POST',))
def post():
    """
    Route for uploading "big data" to database

    Request should be json, contain a simple dict with entries for any data to be uploaded,
    matching options from 'data_types'

    :return: status of request, if true contains how many were inserted
    """

    status = {
        'success': True,
    }
    if not request.is_json:
        status['success'] = False
        return status
    database = db.get_db().get_database('big_data')
    inserted = 0
    for data_type in data_types:
        if data_type in request.json:
            ins = {
                'datetime': datetime.now(),
                'data': request.json[data_type]
            }
            database.get_collection(data_type).insert_one(ins)
            inserted += 1
    status['inserted'] = inserted
    return status
