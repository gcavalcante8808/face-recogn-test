
import pdb
import os
import face_recognition

known_image = face_recognition.load_image_file("base.jpg")
biden_encoding = face_recognition.face_encodings(known_image)[0]

results = list()
for filename in os.listdir('unknown/'):
    unknown_image = face_recognition.load_image_file('unknown/{}'.format(filename))
    unknown_encoding = face_recognition.face_encodings(unknown_image)
    if not unknown_encoding:
        continue
    results.append(face_recognition.compare_faces([biden_encoding], unknown_encoding[0]))

print(len(results))