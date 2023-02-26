from ...monogodb import db
from bson.objectid import ObjectId
from bson.json_util import dumps

collection = db["klsworld_person"]


def fromID(id):
    return collection.find_one({"_id": ObjectId(id)})


def fromLabelname(labelname):
    return collection.find_one({"labelname": labelname})


def fromNickname(nickname):
    return collection.find_one({"nickname": nickname})


def allPosition(position):
    return collection.find({"position":position})


def wordChangedText(text):


    li = allPosition("maid")

    for item in li:
        person = dumps(item)
        print("person", person)
        print("name", item["labelname"], item["synonyms"])
