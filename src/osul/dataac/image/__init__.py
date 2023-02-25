from ...dataac import fromID
from urllib.request import urlopen
from PIL import Image

host = "http://miyo2020.cafe24.com"


def imageUrl(id):
    image = fromID(id)
    print("image", image)
    # ${acfile.imageUrl}${image.path}/${image.id}.${image.exa}`
    if image is not None:
        return f"{host}/acfile/data/{image['path']}/{str(image['_id'])}.{image['exa']}"
    return None
