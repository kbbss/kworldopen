import uuid

from ....stablediffusion import makeImagePipe
from pytz import timezone
import datetime
from bson.objectid import ObjectId
from bson.json_util import dumps
import time
from ....dataac.image import sample as image_sample
import threading
from ....monogodb import db

collection = db["klsworld_targetshape_aiimages"]

class AIImageApp:
    from ....stablediffusion import makeImagePipe
    from ....dataac.image import upload
    import requests



    host = "http://kebiat.iptime.org:8082"
    model_name = "Manseo/Colorful-v4.5-Plus"

    pipe = makeImagePipe(model_name)

    def info(self):
        return {"version": "0.0.1"}

    def create(self, params):
        params["createdate"] = datetime.datetime.now(timezone('Asia/Seoul'))
        print("create!!", params)
        id = self.collection.insert(params)
        print("aiimage id", str(id))
        params["id"] = str(id)
        return params

    def updateImage(self, id, imageID):
        return self.collection.update_one({"_id": ObjectId(id)}, {"$set": {"image": imageID}})

    def updateState(self, id, state):
        return self.collection.update_one({"_id": ObjectId(id)}, {"$set": {"state": state}})


class AiImagesT(threading.Thread):

    def __init__(self, aiImageApp, aiimages):
        threading.Thread.__init__(self)
        self.aiimages = aiimages
        self.aiImageApp = aiImageApp

    def run(self):
        update = self.aiImageApp.updateState(self.aiimages["id"], "generating")
        from ....dataac.image import upload

        print("self.aiimges", self.aiimages)

        prompt = self.aiimages["prompt"]
        model_name = self.aiimages["model_name"]
        print("prompt=", prompt, "model_name=", model_name)

        self.aiimages["model_name"] = model_name

        pipe = self.aiImageApp.pipe

        filepath = f"./targetshape_aiimage_{self.aiimages['id']}.png"

        image = pipe(prompt).images[0]
        image.save(filepath)

        clist = upload(filepath, "/sdtest")
        image = None
        print("clist", clist)
        for c in clist["list"]:
            image = c

        print("image!", image)
        print("updateImage!!", self.aiimages["id"], str(image["_id"]))
        update = self.aiImageApp.updateImage(self.aiimages["id"], str(image["_id"]))
        print("update image", update)
        update = self.aiImageApp.updateState(self.aiimages["id"], "complete")
        print("update state complete", update)


def run():
    from pyngrok import ngrok
    from flask import Flask, request
    from flask_ngrok import run_with_ngrok
    import requests
    from bson.json_util import dumps
    import json

    aiImageApp = AIImageApp()
    print(f".....................aiiImageApp ... {aiImageApp.info()}")

    print("check", aiImageApp.model_name, aiImageApp.pipe)

    HOST_OSUL_SERVER = "http://kebiat.iptime.org:8082"

    ngrok.set_auth_token("2MDs2nO6RHjqSX7fqnx9Akt4QNM_3Z8XZbFz8NAvGAtVgnfc5")
    app = Flask(__name__)
    run_with_ngrok(app)  # Start ngrok when app is run

    @app.route("/")
    def hello():
        return "Hello World!"

    @app.before_request
    def before_request():
        global url
        url = request.url
        print("url1", url)
        # url = url.replace('http://', 'https://', 1)
        u = url.split('.ngrok.io')[0]
        u += '.ngrok.io'
        print("u!", u)
        if url == f"{u}/":
            print("/...........")
            res = requests.post(f"{HOST_OSUL_SERVER}/klsworld/targetshape/aiimage/host/set",
                                headers={'Content-type': 'application/json'}, json={"host": u})

            print("send host! ", res.json())

    @app.route("/aiimage/create", methods=['POST'])
    def aiimage_create():
        params = json.loads(request.get_data())
        print("aiimage_create...", params)
        print("time.sleep...")

        aiiamges = aiImageApp.create(params)

        aiiamgesT = AiImagesT(aiImageApp, aiiamges)
        aiiamgesT.start()
        return dumps(aiiamges)

    @app.route("/aiimage/sessions", methods=['POST'])
    def sessions():
        return dumps({"sessions": aiImageApp.getSessions()})

    app.run()
