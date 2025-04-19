from pymongo.synchronous.database import Database


class Obj:
    def __init__(self,db: Database, list_name: str, dictionary: dict):
        self.id: str = dictionary["_id"]
        self.db: Database = db
        self.list_name: str = list_name




def new_obj(db: Database, list_name: str,class_name: str, dictionary: dict):
    obj1 = eval(f"{dictionary["_class"]}(db, list_name, dictionary)")
    return obj1