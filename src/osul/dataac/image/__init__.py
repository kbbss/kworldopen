from ...dataac import fromID
from urllib.request import urlopen
from PIL import Image
import numpy as np
import urllib.request
import requests
import cv2
from ...monogodb import db
from bson.objectid import ObjectId
from bson.json_util import dumps

host = "http://miyo2020.cafe24.com"

collection = db["dataac_acfile"]


def imageUrl(id):
    image = fromID(id)
    print("image", image)
    # ${acfile.imageUrl}${image.path}/${image.id}.${image.exa}`
    if image is not None:
        return f"{host}/acfile/data/{image['path']}/{str(image['_id'])}.{image['exa']}"
    return None


def imageShow(id):
    import sys
    IN_COLAB = 'google.colab' in sys.modules

    if IN_COLAB:
        from google.colab.patches import cv2_imshow
        url = imageUrl(id)
        print("url", url)
        if url:
            resp = urllib.request.urlopen(url)
            image = np.asarray(bytearray(resp.read()), dtype='uint8')
            ar = cv2.imdecode(image, cv2.IMREAD_COLOR)
            cv2_imshow(ar)
    else:
        url = imageUrl(id)
        print("url", url)
        if url:
            image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
            image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
            print(image.shape)
            cv2.imshow(f'ImageView ID : {id}', image)
            cv2.waitKey(0)
        return None


def upload(filepaths, cloudpath):
    """
 data = str({"path":"/image"})
files = open('aaa.jpg', 'r')

upload = {'file':files}
res = requests.post("http://miyo2020.cafe24.com/klsworld/acfile/upload/dataac_acfile/upload_files",  files = upload ,data={"param":data})
print("res.json",res.json())
    """
    import requests
    files = {}
    count = 0
    if type(filepaths) == str:
        filepaths = [filepaths]
    for filepath in filepaths:
        print("filepath", filepath)
        file = open(filepath, 'rb')
        print("file", file)
        if file:
            count = count + 1
            files[f"file{count}"] = file
    if len(files) > 0:
        res = requests.post(f"{host}/klsworld/acfile/upload/dataac_acfile/upload_files",
                            files=files, data={"param": str({"path": cloudpath})})
        return res.json()


def sample(path, size=1):
    l = collection.aggregate([{'$match': {"path": path}}, {"$sample": {"size": size}}])
    return l
