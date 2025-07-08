# app/__init__.py

from flask import Flask
from pymongo import MongoClient

from app.config.default import Config

from app.routes.user_routes import user_bp

db = None


# app 관련 설정
def create_app():
    global db
    app = Flask(__name__)
    # config에서 설정파일 가져옴
    app.config.from_object(Config)
    client = MongoClient(app.config["MONGO_URI"])
    db = client.get_database()
    # app.config에 db정보 저장
    # 현재는 로컬의 test DB 사용중
    app.config["DB"] = db

    # user.router에 있는 주소들 앞에 users 고정 역할
    app.register_blueprint(user_bp, url_prefix="/users")

    return app
