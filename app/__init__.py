from flask import Flask
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s (%(module)s)] %(levelname)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default',
    }, 'file': {
        'class': 'logging.FileHandler',
        'filename': 'flightbooker.log',
        'formatter': 'default',}},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'file']
    }
})

app = Flask(__name__)

from app import routes
