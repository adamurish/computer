import pymongo
from flask import g, current_app


def get_db():
    mongo_url = 'mongodb://mongo-container:27017'
    if current_app.env == 'development':
        mongo_url = 'mongodb://localhost:27017'
    if 'db' not in g:
        g.db = pymongo.MongoClient(mongo_url)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
