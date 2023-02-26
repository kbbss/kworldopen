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
    text =changeText(text)
    img = sd_makeImage(model_name, text)
    return img


def changeText(model_name,prompt):
    from ...klsworld.person import allPosition
    maids = allPosition("maid")
    maidtexts =[]
    for maid in maids:
        ts =  find(model_name,{"id": maid["_id"], "name":"person" })
        print("ts",ts)
        if ts :
            maidtexts.append( {"word": maid["labelname"] , "text":  ts["prompt"] })
            maidtexts.append({"word": maid["nickname"], "text": ts["prompt"]})
            for syn in maid["synonyms"]:
                maidtexts.append({"word": syn, "text": ts["prompt"]})
    print("maidtexts",maidtexts)

    def checkhange(text):
        for item in maidtexts:
            if text ==item["word"] :
                return item["text"]
        return text


    ar = prompt.split()

    print("ar", ar)

    rp = ""
    for str in ar:
        str = str.strip()
        comar = str.split(",")
        print("comar len ", str, "=>", len(comar))
        if len(comar) == 1:
            print("comar=1", str)
            if len(rp) != 0:
                rp = rp + " "
            print("!!!!!!!!!!", str)
            rp = rp + checkhange(str)
            print("...rp", rp)
        elif len(comar) > 1:
            print("comar>1", comar)
            cstr = ""
            for cw in comar:
                cw = cw.strip()
                if cw != "":
                    if cstr != "":
                        cstr = cstr + ","
                    print("!!!!!!!!!!", cw)
                    cstr = cstr + checkhange(cw)
                    print("..cstr", cstr)
            if len(rp) != 0:
                rp = rp + " "
            rp = rp + cstr
            print("...rp", rp)

    print("result rp", rp)

    return rp
