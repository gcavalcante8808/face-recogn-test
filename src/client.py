import requests
import asyncio
import os
import pandas as pd


from collections import Counter


url = 'http://localhost:5000'

execution_time = list()
execution_results = list()
async def submit_image(filename):
    files = {'file': open('unknown/{}'.format(filename), 'rb')}
    response = requests.post(url, files=files)
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
