from bson import ObjectId
from pymongo.synchronous.database import Database


class Dict:
    def __init__(self,db: Database, list_name: str, mongoid: str, is_in_list: bool = True):
        self.id: str = mongoid
        self.db: Database = db
        self.list_name: str = list_name
        self.is_in_list: bool = is_in_list
        self.key: str = ""

    def __getitem__(self, item: str):
        if self.is_in_list:
            return self.db[self.list_name].find_one({"_id": ObjectId(self.id)}, {item: 1})[item]
        else:
            return self.db[self.list_name].find_one({"_key": self.key}, {item: 1})[item]

    def __setitem__(self, key: str, value):
        if self.is_in_list:
            self.db[self.list_name].update_one({"_id" : ObjectId(self.id)}, {"$set" : {key: value}})
        else:
            self.db[self.list_name].update_one({"_key": self.key}, {"$set": {key: value}})
