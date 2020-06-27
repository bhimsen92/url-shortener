from config import Config
from flask import Flask
from app.api.api import api_blueprint
from db import setup_db
from snowflake.client import setup_snowflake_client


def create_app(config_class=Config):
    app = Flask(__name__)
    app.register_blueprint(api_blueprint, url_prefix="/")

    # setup db.
    setup_db(config_class)

    # setup snowflake client connection.
    setup_snowflake_client(config_class)

    return app
