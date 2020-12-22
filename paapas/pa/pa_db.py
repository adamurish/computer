from paapas.db import get_db
from paapas.pa import options


def add_to_db(collection, content):
    """
    Add one item to a collection in the database

    :param collection: the collection to add to
    :param content: the item to insert
    """

    db = get_db().get_database('home_automation')
    db.get_collection(collection).insert_one(content)


def get_from_db(collection, filter=None):
    """
    Get all items in a certain collection in the database, with labels

    :param collection: the collection to pull from
    :param filter: the filter to use, default None
    :return: filtered list of items in collection, with added labels for html template usage
    """

    ret = []
    for entry in get_from_db_raw(collection, filter):
        entry['labels'] = {}
        for field in options[collection]:
            entry['labels'][field] = str.capitalize(field)
        ret.append(entry)
    return ret


def get_from_db_raw(collection, filter=None):
    """
    Get all items in a certain collection in the database, without labels

    :param collection: the collection to pull from
    :param filter: the filter to use, default None
    :return: filtered items in collection, in a mongoDB cursor reference
    """

    db = get_db().get_database('home_automation')
    return db.get_collection(collection).find(filter)