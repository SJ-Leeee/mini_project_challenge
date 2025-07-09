from datetime import datetime
from flask import current_app
from bson.objectid import ObjectId


def get_challenge_by_id_with_userId(challenge_id, user_id):
    try:
        db = current_app.config["DB"]
        challenge_collection = db["challenges"]

        query = {
            "_id": ObjectId(challenge_id),
            "user_id": ObjectId(user_id),
        }
        challenge = challenge_collection.find_one(query)
        print(challenge)
        return challenge
    except Exception as e:
        # 데이터베이스 오류 또는 기타 예상치 못한 오류
        raise ValueError(f"{str(e)}")


def post_record_model(oneline_diary, photo_url, challenge):
    try:
        db = current_app.config["DB"]
        record_collection = db["record"]
        today = datetime.today().strftime("%m%d")

        record = {
            "challenge_id": challenge["_id"],
            "oneline_diary": oneline_diary,
            "photo_url": photo_url,
            "created_date": today,
        }

        result = record_collection.insert_one(record)
        print(result)
        return result
    except Exception as e:
        # 데이터베이스 오류 또는 기타 예상치 못한 오류
        raise e


def get_record_by_challenge_id_with_today(challenge_id):

    try:
        print("?ASd")
        db = current_app.config["DB"]
        record_collection = db["record"]
        today = datetime.today().strftime("%m%d")
        query = {"challenge_id": challenge_id, "created_date": today}

        record = record_collection.find_one(query)
        return record
    except Exception as e:
        # 데이터베이스 오류 또는 기타 예상치 못한 오류
        raise e
