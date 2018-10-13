import multiprocessing
import jsonlogging
import logging
import os

SERVER_PORT = os.getenv('SERVER_PORT', 5000)
bind = "0.0.0.0:{}".format(SERVER_PORT)
#workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
worker_connections = 512
worker_class = 'gevent'
timeout = 30
backlog = 512

daemon = False
pidfile = None
umask = 0
user = None
group = None

#logger_class = 'jsonlogging.JSONFormatter'
tmp_upload_dir = None
errorlog = '-'
loglevel = 'info'
#accesslog = '-'
#access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'