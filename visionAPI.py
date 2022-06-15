from cProfile import label
import io
import os


def vision(url):
# Set environment variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "schoolpj-eec77e4b1050.json"

# Imports the Google Cloud client library
    from google.cloud import vision

# Instantiates a client
    client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
    file_name = os.path.abspath(url)

# Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

# Performs label detection on the image file
#    response = client.label_detection(image=image)
#    labels = response.label_annotations
    
# Performs text detection on the image file
    response = client.text_detection(image=image)
    texts = response.text_annotations
#    text_list = list(map(lambda x: x.description, texts))

    str = ''

    for text in texts:
        str += text.description
    return str
