from ...monogodb import db
from bson.objectid import ObjectId

collection = db["klsworld_shapeword"]


def fromList(category):
    return collection.find({"category": category})


"""
db.collection.aggregate(
  { $sample: { size: 1 } }
)
"""


def categroySample(category):
    l= collection.aggregate([{'$match': {"category": category}}, {"$sample": {"size": 1}}])
    for data in l:
        return data

def randomText():
    job = categroySample("job")
    place = categroySample("place")
    emotion =categroySample("emotion")
    return f"{job['name']},{place['name']},{emotion['name']}"