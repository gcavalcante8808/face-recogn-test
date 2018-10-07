import asyncio
import os
import face_recognition
import datetime

known_image = face_recognition.load_image_file("base.jpg")
biden_encoding = face_recognition.face_encodings(known_image)[0]

results = list()
    
async def verify_image(filename):
    unknown_image = face_recognition.load_image_file('unknown/{}'.format(filename))
    unknown_encoding = face_recognition.face_encodings(unknown_image)
    if unknown_encoding:
        results.append(face_recognition.compare_faces([biden_encoding], unknown_encoding[0]))

async def main(loop):
    images = (filename for filename in os.listdir('unknown/'))
    tasks = [verify_image(image) for image in images]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    print(results)
