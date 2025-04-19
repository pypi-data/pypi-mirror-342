As we all know, MongoDB is a very good nosql database, but pymongo is a **violent transplant from C# binding**.
This project repackages pymongo, making full use of dynamic type features to make MongoDB more **pythonic**.

Currently supported functions

1. You can access MongoDB like using **list** and **dict**, and it takes up almost no memory.

```
db = pymongo.MongoClient()
list1 = mongohelper.operator.List(db["test"], "test")
list1.append({"aaa" : 123, "sadasd": "dasdas"})
list1["68026c54e4e6b28563e2bc48"]["aaa"] = 666
print(list1["68026c54e4e6b28563e2bc48"]["aaa"])
for dictionary in list1:
    print(dictionary["aaa"])
```