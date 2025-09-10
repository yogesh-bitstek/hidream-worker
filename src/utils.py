import io
import base64
from PIL import Image

def image_to_base64(image):
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def base64_to_image(b64_string):
    return Image.open(io.BytesIO(base64.b64decode(b64_string)))