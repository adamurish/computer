import pymongo
from flask import g
from paapas.pa import options


def get_db():
    if 'db' not in g:
        g.db = pymongo.MongoClient('mongodb://localhost:27017')
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
