from ...monogodb import db
from bson.objectid import ObjectId

collection = db["klsworld_person"]


def fromID(id):
    return collection.find_one({"_id": ObjectId(id)})


def fromLabelname(labelname):
    return collection.find_one({"labelname": labelname})


def fromNickname(nickname):
    return collection.find_one({"nickname": nickname})
