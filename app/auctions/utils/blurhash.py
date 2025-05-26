import requests
import blurhash
import numpy as np
from io import BytesIO
from PIL import Image as pil_image

def generate_blurhash(image_url:str)-> str:
    image = pil_image.open(BytesIO(requests.get(image_url).content))
    image.thumbnail((100,100))
    numpy_image = np.array(image)
    hash = blurhash.encode(numpy_image, components_x=4, components_y=3)
    print(hash)

    return hash