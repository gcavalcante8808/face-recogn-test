from flask import Flask, request
from werkzeug import secure_filename


import face_recognition

app = Flask(__name__)
known_image = face_recognition.load_image_file("base.jpg")
biden_encoding = face_recognition.face_encodings(known_image)[0]

@app.route('/', methods = ['POST'])
def index():
    f = request.files['file']
    unknown_image = face_recognition.load_image_file(f)
    unknown_encoding = face_recognition.face_encodings(unknown_image)
    if unknown_encoding:
        comp = face_recognition.compare_faces([biden_encoding], unknown_encoding[0])
        if comp:
            return "Face Recognized"

    return "Face not Recognized"

if __name__ == '__main__':
    app.run(debug = True)
