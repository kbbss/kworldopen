from src.osul.monogodb import db
from bson.objectid import ObjectId

collection = db["dataac_acfile"]


def fromID(id):
    return collection.find_one({"_id": ObjectId(id)})
