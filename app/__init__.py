# app/__init__.py

from flask import Flask
from pymongo import MongoClient

from app.config.default import Config


from app.routes.user_routes import user_bp
from app.routes.rendering_routes import rendering_bp
from app.routes.challenge_routes import challenge_bp
from app.routes.record_routes import record_bp
from app.routes.file_routes import file_bp

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

    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

    # url고정 및 라우트 등록
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(challenge_bp, url_prefix="/api/challenge")
    app.register_blueprint(record_bp, url_prefix="/api/record")
    app.register_blueprint(file_bp, url_prefix="/api/file")

    app.register_blueprint(rendering_bp)

    return app
