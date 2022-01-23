import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="PATH_TO_JSON_CONTAINING_API_HASH"

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    str_to_ret = ""

    for text in texts:
        str_to_ret += '"{}"'.format(text.description.strip().strip("\n")).strip() + " "

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        str_to_ret += '{}\n'.format(' '.join(vertices))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return str_to_ret.strip("\n")

# print(detect_text("dataset/test/TEST_0006.jpg"))

import glob
from os.path import exists

os.chdir("dataset/validation")
errored = open("coords/errored.txt", "w")

arr = glob.glob("*.jpg")
arr.reverse()
for filename in arr:

    try:
        newfn = "coords/" + filename.split(".")[0] + ".cropinfo"
        if exists(newfn) and os.stat(newfn).st_size != 0:
            continue
        #print(newfn)
        fl = open(newfn, "w")
        fl.write(detect_text(filename))
        fl.close()
    except Exception as e:
        print(filename)
        print(e)
        errored.write(filename)
errored.close()
