from ...monogodb import db
from bson.objectid import ObjectId

collection = db["klsworld_shapeword"]


def fromList(category):
    return collection.find({"category": category})


def categroySample(category):
    l = collection.aggregate([{'$match': {"category": category}}, {"$sample": {"size": 1}}])
    for data in l:
        return data


def randomText():
    job = categroySample("job")
    place = categroySample("place")
    emotion = categroySample("emotion")
    return f"{job['name']},{place['name']},{emotion['name']}"


def creteRandomImage():
    import requests
    from ...stablediffusion import makeImage
    from ...dataac.image import upload
    from bson.json_util import dumps
    host = "http://kebiat.iptime.org:8082"
    res = requests.post(f"{host}/klsworld/shapeword/makeimage/request_data",
                        headers={'Content-type': 'application/json'}, json={})
    json = res.json()
    print("request_data", json)

    prompt = json["prompt"]
    type = json["type"]
    print("prompt=", prompt, "type=", type)

    image = makeImage("Linaqruf/anything-v3.0", prompt)
    image.save("result.jpg")

    clist = upload("result.jpg", "/sdtest")
    print("clist", clist)
    for c in clist["list"]:
        json["image"] = c["id"]

    res = requests.post(f"{host}/klsworld/shapeword/makeimage/create",
                        headers={'Content-type': 'application/json'}, json=json)

    made = res.json()
    print("made", made)
    return {"image": image, "made": made}
