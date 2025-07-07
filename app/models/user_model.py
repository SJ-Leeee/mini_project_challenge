from bson import ObjectId
from app import db


def insert_user(user_data):
    result = db["users"].insert_one(user_data)
    return str(result.inserted_id)


def get_user_by_id(user_id):
    return db["users"].find_one({"_id": ObjectId(user_id)})
