from ...monogodb import db
from bson.objectid import ObjectId
from ...stablediffusion import makeImage as sd_makeImage
from ...dataac.image import upload

collection = db["klsworld_targetshape"]


def find(model_name, target):
    return collection.find_one(
        {"model_name": model_name, "target._id": ObjectId(target["id"]), "target.name": target["name"]})


def createImage(model_name, target):
    ts = find(model_name, target)
    print("ts",ts)
    if ts:
        img = sd_makeImage(model_name,ts["prompt"])
        if img:
            filename = "targetshape_create_image.jpg"
            img.save(filename)

            clist= upload(filename, "/sdtest")
            print("clist",clist)
            return img

    else:
        print(f"targetshapenone model_name={model_name} ,target={target}")
        return None
