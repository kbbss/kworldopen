from ...monogodb import db
from bson.objectid import ObjectId
from ...stablediffusion import makeImage as sd_makeImage
from ...dataac.image import upload

collection = db["klsworld_targetshape"]


def find(model_name, target):
    return collection.find_one(
        {"model_name": model_name, "target._id": ObjectId(target["id"]), "target.name": target["name"]})


def createImage(model_name, target, another_prompt=""):
    ts = find(model_name, target)
    print("ts", ts)
    if ts:
        prompt = ts["prompt"]
        if len(another_prompt) > 0:
            prompt = f"{prompt},{another_prompt}"
        img = sd_makeImage(model_name, prompt)
        if img:
            filename = "targetshape_create_image.jpg"
            img.save(filename)

            clist = upload(filename, "/sdtest")
            print("clist", clist)
            return img

    else:
        print(f"targetshapenone model_name={model_name} ,target={target}")
        return None


def createPromptImage(model_name, text):
    text = changeText(model_name, text)
    print("changetext..", text)
    img = sd_makeImage(model_name, text)
    if img:
        filename = "targetshape_create_image.jpg"
        img.save(filename)

        clist = upload(filename, "/sdtest")
        print("upload!", clist)
    return img


def changeText(model_name, prompt):
    from ...klsworld.person import allPosition
    maids = allPosition("maid")
    maidtexts = []
    for maid in maids:
        ts = find(model_name, {"id": maid["_id"], "name": "person"})

        if ts:
            maidtexts.append({"word": maid["labelname"], "text": ts["prompt"]})
            maidtexts.append({"word": maid["nickname"], "text": ts["prompt"]})
            for syn in maid["synonyms"]:
                maidtexts.append({"word": syn, "text": ts["prompt"]})

    def checkhange(text):
        for item in maidtexts:
            if text == item["word"]:
                return item["text"]
        return text

    ar = prompt.split()
    rp = ""
    for str in ar:
        str = str.strip()
        comar = str.split(",")
        if len(comar) == 1:
            if len(rp) != 0:
                rp = rp + " "
            rp = rp + checkhange(str)
        elif len(comar) > 1:
            cstr = ""
            for cw in comar:
                cw = cw.strip()
                if cw != "":
                    if cstr != "":
                        cstr = cstr + ","
                    cstr = cstr + checkhange(cw)
            if len(rp) != 0:
                rp = rp + " "
            rp = rp + cstr
    return rp


def makeAIImage(model_name, size=1):
    from ...stablediffusion import makeImagePipe
    from ...dataac.image import upload
    import requests
    host = "http://kebiat.iptime.org:8082"

    pipe = makeImagePipe(model_name)

    for i in range(size):
        filepath = f"./r{str(i + 1).zfill(3)}.png"
        print(f"makeimage..... {filepath}")
        res = requests.post(f"{host}/klsworld/targetshape/schedule/request",
                            headers={'Content-type': 'application/json'}, json={})
        json = res.json()
        print("request json", json)
        prompt = json["prompt"]
        json["model_name"] = model_name

        image = pipe(prompt).images[0]
        image.save(filepath)

        clist = upload(filepath, "/sdtest")
        print("clist", clist)
        for c in clist["list"]:
            json["image"] = c["id"]

        res = requests.post(f"{host}/klsworld/targetshape/schedule/create",
                            headers={'Content-type': 'application/json'}, json=json)

        aiimage = res.json()
        print("aiimage", aiimage)

    return ""
