# coding: utf-8
from bson import objectid
from pymongo import MongoClient


class Mongo:

    def __init__(self, app=None):
        self._mongo_client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        mongo_url = app.config.get("MONGODB_URL", "mongodb://localhost:27017")
        self._mongodb_client = MongoClient(mongo_url)

    @property
    def client(self):
        return self._mongodb_client

    def select_db(self, db_name):
        return getattr(self.client, db_name)

    def select_collection(self,  db_name, collection_name):
        return self.select_db(db_name)[collection_name]

    def insert(self, collection, data):
        obj_id = collection.insert_one(data).inserted_id
        return str(obj_id)

    def update(self, collection, condition, data):
        obj_id = collection.update_one(condition, data).ObjectId
        return str(obj_id)
