import pymongo
from flask import g


def get_db():

    if 'db' not in g:
        g.db = pymongo.MongoClient('mongodb://mongo-container:27017')
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
