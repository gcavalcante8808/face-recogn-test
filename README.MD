Face Recognition Test
---------------------

This is test for Face Recognition lib using DLIB + MKL + AVX Support through a flask app and a client.

## Requirements

Docker and Docker-Compose installed and working.

## HowToUse

Clone this repository and use the command `docker-compose up -d` inside the cloned folder to start the server.

After that, you just need to fire the `client.py` through the command:

```
    docker-compose exec face python client.py
```

## How to change base image

Just overwrite the `known/base.jpg` (which is jonatahan goldsmith by default) file with the desired face.

## How to test more images

Just put the desired images in the unknown dir.

