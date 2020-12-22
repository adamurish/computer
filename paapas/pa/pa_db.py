from paapas.db import get_db
from paapas.pa import options


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


def get_from_db_raw(collection, filter=None):
    db = get_db().get_database('home_automation')
    return db.get_collection(collection).find(filter)