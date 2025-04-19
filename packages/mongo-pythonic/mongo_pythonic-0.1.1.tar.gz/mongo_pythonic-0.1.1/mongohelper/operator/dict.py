from bson import ObjectId
from pymongo.synchronous.database import Database


class Dict:
    def __init__(self,db: Database, list_name: str, mongoid: str):
        self.id: str = mongoid
        self.db: Database = db
        self.list_name: str = list_name

    def __getitem__(self, item: str):
        return self.db[self.list_name].find_one({"_id": ObjectId(self.id)}, {item: 1})[item]

    def __setitem__(self, key: str, value):
        self.db[self.list_name].update_one({"_id" : ObjectId(self.id)}, {"$set" : {key: value}})
