import uuid

from ....stablediffusion import makeImagePipe
from pytz import timezone
import datetime


class AIImageApp:
    from ....monogodb import db

    collection = db["klsworld_targetshape_aiimages"]

    def info(self):
        return {"version": "0.0.1"}

    def create(self, params):
        print("create!!", params)
        params["createdate"] = datetime.datetime.now(timezone('Asia/Seoul'))
        id = self.collection.insert(params)
        print("aiimage id", str(id))
        params["id"] = str(id)
        return params

    def getSessions(self):
        return self.sar


def run():
    from pyngrok import ngrok
    from flask import Flask, request
    from flask_ngrok import run_with_ngrok
    import requests
    from bson.json_util import dumps
    import json

    aiImageApp = AIImageApp()
    print(f".....................aiiImageApp ... {aiImageApp.info()}")

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
        return dumps(aiImageApp.create(params))

    @app.route("/aiimage/sessions", methods=['POST'])
    def sessions():
        return dumps({"sessions": aiImageApp.getSessions()})

    app.run()
