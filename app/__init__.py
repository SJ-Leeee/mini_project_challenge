# app/__init__.py

from flask import Flask
from pymongo import MongoClient

# from app.config.default import Config
# from app.routes.user_routes import user_bp

db = None


def create_app():
    global db
    app = Flask(__name__)
    # app.config.from_object(Config)

    client = MongoClient(app.config["MONGO_URI"])
    db = client.get_database()

    # app.register_blueprint(user_bp)

    return app
