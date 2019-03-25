import base64
import time
import json
import os

import falcon
import face_recognition

from werkzeug.serving import run_simple
from io import BytesIO

from middleware import MatchResultLoggingMiddleware
from storage import s3_client as storage

server_port = os.getenv('SERVER_PORT', 5000)

#Preload Base Image.
known_image = face_recognition.load_image_file("base.jpg")
biden_encoding = face_recognition.face_encodings(known_image)[0]


class ImageDetectionResource(object):
    def on_post(self, req, resp):
        """
        Get some info from json request, transform base64 into image
        and make the face_compare.
        """
        identity = req.media.get('identity', False)
        client = req.media.get('client', 'unknown')
        filename = req.media.get('filename', 'unknown_image')

        image = self.base64toimage(identity, req)
        unknown_encoding = self.get_face_encondings(image, req)
        if unknown_encoding:
            comp = self.compare_faces(unknown_encoding, req)
            if comp:
                resp.body = json.dumps({"matched": True, "person": "Jhonatan GoldSmith"})
            else:
                resp.body = json.dumps({"matched": False, "person": None})

        self.save_to_storage(image, filename, req)
        resp.status = falcon.HTTP_200

    def base64toimage(self, encoded, req):
        """
        Convert base64string into bytes like img.
        """
        base = base64.b64decode(encoded)
        
        return base

    def get_face_encondings(self, image, req):
        unknown_image = face_recognition.load_image_file(BytesIO(image))
        unknown_encoding = face_recognition.face_encodings(unknown_image)

        return unknown_encoding

    def compare_faces(self, unknown_encoding, req):
        comp = face_recognition.compare_faces([biden_encoding], unknown_encoding[0])
        return comp

    def save_to_storage(self, image, filename, req):
        """
        Send binary file to storage.
        """
        storage.upload_fileobj(BytesIO(image), filename)


app = falcon.API(middleware=[
    MatchResultLoggingMiddleware(),
])

resources = ImageDetectionResource()
app.add_route('/', resources)

if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)
