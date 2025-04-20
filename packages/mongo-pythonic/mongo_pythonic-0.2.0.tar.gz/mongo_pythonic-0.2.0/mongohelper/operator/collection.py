from typing import Generator

from bson import ObjectId
from pymongo.synchronous.database import Database

from mongohelper.operator import Dict


class Collection:
    def __init__(self, db: Database, name: str):
        self.db: Database = db
        self.name: str = name

        if not self.name in db.list_collection_names():
            db.create_collection(name)

    def __getitem__(self, item: str) -> Dict:
        result: dict = self.db[self.name].find_one({"_key" : item}, {"_id" : 1})
        dictionary: Dict = Dict(self.db, self.name, str(result["_id"]), False)
        dictionary.key = item

        return dictionary

    def __setitem__(self, key: str, value: dict):
        value1: dict = value.copy()
        value1["_key"] = key

        self.db[self.name].find_one_and_replace({"_key" : key}, value1, upsert=True)

    # def __iter__(self) -> Generator[Dict, Any, None]:
    #     for cursor in self.traverse():
    #         yield Dict(self.db, self.name, str(cursor["_id"]))
