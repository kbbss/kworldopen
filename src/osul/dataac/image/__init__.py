from ...dataac import fromID
from urllib.request import urlopen
from PIL import Image
import numpy as np
import urllib.request
import cv2

host = "http://miyo2020.cafe24.com"


def imageUrl(id):
    image = fromID(id)
    print("image", image)
    # ${acfile.imageUrl}${image.path}/${image.id}.${image.exa}`
    if image is not None:
        return f"{host}/acfile/data/{image['path']}/{str(image['_id'])}.{image['exa']}"
    return None


def imageCv2Array(id):
    url = imageUrl(id)
    if url is not None:
        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype='uint8')
        return cv2.imdecode(image, cv2.IMREAD_COLOR)
    return None
