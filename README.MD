Face Recognition Test
---------------------

This is a joker project to test Face Recognition library. It has the following configurations/behaviours:
 
  * Face Recognition lib using DLIB + MKL + AVX Support through a falcon endpoint;
  * Python LogBook;
  * Automatic logging with fluentd + docker + elasticsearch;
  * Backup on S3 using Minio.

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

## How to Visualize Logs

Access the Kibana in the `localhost:5601` and click on Discover Tab: the application logs will be persisted in json
format inside the elasticsearch.

## How it Works

**TODO**