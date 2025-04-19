from typing import Any, Mapping, Generator

from bson import ObjectId
from chromadb.db.base import Cursor
from pymongo.synchronous.cursor import Cursor
from pymongo.synchronous.database import Database

from mongohelper.operator import Dict
from .dict import Dict


class List:
    def __init__(self, db: Database, name: str):
        self.db: Database = db
        self.name: str = name

        if not self.name in db.list_collection_names():
            db.create_collection(name)

    def __getitem__(self, item: str) -> Dict:
        result: dict = self.db[self.name].find_one({"_id" : ObjectId(item)}, {"_id" : 1})
        dictionary: Dict = Dict(self.db, self.name, str(result["_id"]))

        return dictionary

    def __setitem__(self, key: str, value: dict):
        self.db[self.name].find_one_and_replace({"_id" : ObjectId(key)}, value)

    def __iter__(self) -> Generator[Dict, Any, None]:
        for cursor in self.traverse():
            yield Dict(self.db, self.name, str(cursor["_id"]))


    def append(self, dictionary: dict) -> Dict:
        self.db[self.name].insert_one(dictionary)

        return Dict(self.db, self.name, str(dictionary["_id"]))

    def traverse(self) -> Cursor[Mapping[str, Any] | Any]:
        return self.db[self.name].find()
