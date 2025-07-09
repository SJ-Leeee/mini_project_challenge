# app/__init__.py

from flask import Flask
from pymongo import MongoClient

from app.config.default import Config

from app.routes.user_routes import user_bp
from app.routes.mainpage_routes import main_bp
from app.routes.challenge_routes import challenge_bp
from datetime import datetime

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
    print(datetime.now())

    # user.router에 있는 주소들 앞에 users 고정 역할
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(challenge_bp, url_prefix="/api/challenge")

    app.register_blueprint(main_bp)

    return app
