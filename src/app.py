from flask import Flask
from ext import db
from ext import config
from ext import api
from ext import site
from ext import cli

def create_app():
    app = Flask(__name__)

    config.init_app(app)
    db.init_app(app)
    cli.init_app(app)
    api.init_app(app)
    site.init_app(app)
    
    return app