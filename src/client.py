import requests
import asyncio
import os
import pandas as pd
import base64
import json
import random

from collections import Counter


SERVER_PORT = os.getenv('SERVER_PORT', 5000)

url = 'http://localhost:{}'.format(SERVER_PORT)

clients = ('client1','client2','client3','client4','client5')

execution_time = list()
execution_results = list()
async def submit_image(filename):
    with open('unknown/{}'.format(filename), 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read())

    headers = {'Content-Type':'application/json'}
    data = {'identity': encoded_image.decode('utf-8'), 'client': random.choice(clients), 'filename': filename}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    assert response.status_code, 200

    execution_time.append(response.elapsed.total_seconds())
    execution_results.append(response.text)

async def main(loop):
    images = (filename for filename in os.listdir('unknown/'))
    tasks = [submit_image(image) for image in images]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    print(Counter(execution_results))
    s = pd.Series(execution_time)
    print(s.describe())
