from bson import ObjectId
from app import db
from flask import current_app


def insert_user(user_data):
    result = db["users"].insert_one(user_data)
    return str(result.inserted_id)


def get_user_by_id(user_id):
    return db["users"].find_one({"_id": ObjectId(user_id)})


# DB에 email이 존재하는지 확인하는 유틸 함수
def is_email_exist(email):
    db = current_app.config["DB"]
    return db.user_info.find_one({"email": email}) is not None
