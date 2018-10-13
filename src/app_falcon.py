import logging
import time
import falcon
import face_recognition
import jsonlogging

from wsgiref import simple_server
from io import BytesIO
from falcon_multipart.middleware import MultipartMiddleware

known_image = face_recognition.load_image_file("base.jpg")
biden_encoding = face_recognition.face_encodings(known_image)[0]

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogging.JSONFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


def timeit(method):
    """
    Applied as an decorator to get time elapsed.
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        data = 'Method: {}, args: {}, kwargs: {}, elapsed: {:f}'.format(method.__name__, args, kw, te-ts)
        logger.warning(data)
        return result

    return timed


class ImageDetectionResource(object):
    @timeit
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
