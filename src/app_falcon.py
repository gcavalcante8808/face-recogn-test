import falcon
import face_recognition

from wsgiref import simple_server
from falcon_multipart.middleware import MultipartMiddleware
from io import BytesIO

known_image = face_recognition.load_image_file("base.jpg")
biden_encoding = face_recognition.face_encodings(known_image)[0]


class ImageDetectionResource(object):
    def on_post(self, req, resp):
        f = req.get_param('file')
        unknown_image = face_recognition.load_image_file(BytesIO(f.file.read()))
        unknown_encoding = face_recognition.face_encodings(unknown_image)
        if unknown_encoding:
            comp = face_recognition.compare_faces([biden_encoding], unknown_encoding[0])
            if comp:
                resp.body = ("Face Recognized")
            else:
                resp.body = ("Face not Recognized")

        resp.status = falcon.HTTP_200

app = falcon.API(middleware=[MultipartMiddleware()])


resources = ImageDetectionResource()
app.add_route('/', resources)

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()

