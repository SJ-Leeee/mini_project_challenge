from bson import ObjectId
from app import db
from flask import current_app


def insert_user(user_data):
    result = db["users"].insert_one(user_data)
    return str(result.inserted_id)


def get_user_by_id(user_id):
    return db["users"].find_one({"_id": ObjectId(user_id)})


def is_email_exist(email):
    """
    주어진 이메일이 DB에 이미 존재하는지 확인합니다.

    Parameters:
        email (str): 중복 확인할 이메일 주소.

    Returns:
        bool: 이미 존재하면 True, 없으면 False.
    """
    db = current_app.config["DB"]
    return db.user_info.find_one({"email": email}) is not None
