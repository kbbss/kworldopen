

def run():
    print("flaskserver...........")
    from pyngrok import ngrok
    from flask import Flask, request
    from flask_ngrok import run_with_ngrok
    import requests
    from bson.json_util import dumps
    import json
    HOST_OSUL_SERVER = "http://kebiat.iptime.org:8082"


    ngrok.set_auth_token("")
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
            res = requests.post(f"{HOST_OSUL_SERVER}/osul/ngrokhost/set_now_host",
                                headers={'Content-type': 'application/json'}, json={"host": u})

    @app.route("/make_image",methods=['POST'] )
    def make_image():
        from ...stablediffusion import makeImage
        from ...dataac.image import upload

        params = json.loads(request.get_data(), encoding='utf-8')
        print("parans", params)
        image = makeImage(params["model_name"], params["prompt"])
        filepath = "makeimage.jpg"
        image.save(filepath)
        clist = upload(filepath, "/sdtest")
        acfile = None
        for c in clist:
            acfile = c

        return dumps({"acfile": acfile})

    app.run()
