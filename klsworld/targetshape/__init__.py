from osul.monogodb import db
from bson.objectid import ObjectId

collection = db["klsworld_targetshape"]

def find(model_name, target):
    return collection.find_one(
        {"model_name": model_name, "target._id": ObjectId(target["id"]), "target.name": target["name"]})