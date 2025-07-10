from flask import current_app
from datetime import datetime, timedelta
from app.utils.enum.ChallengeSortTypeEnum import ChallengeSortType
from bson import ObjectId


def get_public_challenge_model(sort_type):
    try:
        db = current_app.config["DB"]
        challenge_collection = db["challenges"]

        # challenges = list(challenge_collection.find())
        query = {"is_public": True}
        sort_type = ChallengeSortType(sort_type)  # ✅ Enum으로 변환

        if sort_type == ChallengeSortType.LIKE:
            challenges = list(challenge_collection.find(query).sort("like_count", -1))
        elif sort_type == ChallengeSortType.RECENT:
            challenges = list(challenge_collection.find(query).sort("created_at", -1))
        elif sort_type == ChallengeSortType.COMMENT:
            challenges = list(
                challenge_collection.find(query).sort("comment_count", -1)
            )

        for c in challenges:
            c["_id"] = str(c["_id"])
            c["user_id"] = str(c["user_id"])

        return challenges

    except Exception as e:
        # 데이터베이스 오류 또는 기타 예상치 못한 오류
        raise ValueError(f"{str(e)}")


def get_private_challenge_model(sort_type, user_id):
    try:
        db = current_app.config["DB"]
        challenge_collection = db["challenges"]

        sort_type = ChallengeSortType(sort_type)  # ✅ Enum으로 변환

        query = {"user_id": ObjectId(user_id), "is_public": False}

        if sort_type == ChallengeSortType.LIKE:
            challenges = list(challenge_collection.find(query).sort("like_count", -1))
        elif sort_type == ChallengeSortType.RECENT:
            challenges = list(challenge_collection.find(query).sort("created_at", -1))
        elif sort_type == ChallengeSortType.COMMENT:
            challenges = list(
                challenge_collection.find(query).sort("comment_count", -1)
            )

        for c in challenges:
            c["_id"] = str(c["_id"])
            c["user_id"] = str(c["user_id"])

        return challenges

    except Exception as e:
        # 데이터베이스 오류 또는 기타 예상치 못한 오류
        raise ValueError(f"{str(e)}")


def post_challenges_model(challenge_data, user_id):
    try:
        db = current_app.config["DB"]
        challenge_collection = db["challenges"]

        # 날짜 계산
        today = datetime.now()  # ✅ date() 제거
        count = challenge_data["challenge_count"]
        end_date = today + timedelta(days=count)

        challenge = {
            "title": challenge_data["title"],
            "topic": challenge_data["topic"],
            "challenge_count": count,
            "is_public": challenge_data["is_public"],
            "user_id": ObjectId(user_id),
            "like_count": 0,
            "comment_count": 0,
            "photo_url": challenge_data.get("photo_url", ""),
            "start_date": today,  # 2025-07-08
            "end_date": end_date,  # 2025-08-01
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        result = challenge_collection.insert_one(challenge)
        return result

    except Exception as e:
        # 데이터베이스 오류 또는 기타 예상치 못한 오류
        raise ValueError(f"{str(e)}")


def get_user_by_id(user_id):
    try:
        db = current_app.config["DB"]
        user_collection = db["users"]

        user = user_collection.find_one({"_id": ObjectId(user_id)})
        return user
    except Exception as e:
        # 데이터베이스 오류 또는 기타 예상치 못한 오류
        raise ValueError(f"{str(e)}")


def get_challenge_by_id(challenge_id):
    try:
        db = current_app.config["DB"]
        challenge_collection = db["challenges"]

        challnege = challenge_collection.find_one({"_id": ObjectId(challenge_id)})

        return challnege
    except Exception as e:
        # 데이터베이스 오류 또는 기타 예상치 못한 오류
        raise ValueError(f"{str(e)}")


def like_challenge_model(user, challenge):
    try:
        db = current_app.config["DB"]
        likes_collection = db["likes"]
        challenge_collection = db["challenges"]
        query = {"user_id": user["_id"], "challenge_id": challenge["_id"]}

        likes = likes_collection.find_one(query)

        if likes:
            likes_collection.delete_one(query)
            # 좋아요 취소 처리 완료
            challenge_collection.update_one(
                {"_id": challenge["_id"]}, {"$inc": {"like_count": -1}}
            )
            return {"message": "좋아요가 -1 되었습니다."}

        else:
            # 좋아요 등록 로직 (없으면 추가)
            likes_collection.insert_one(query)
            challenge_collection.update_one(
                {"_id": challenge["_id"]}, {"$inc": {"like_count": 1}}
            )
            return {"message": "좋아요가 +1 되었습니다."}

        # challnege = challenge_collection.find_one({"_id": challenge_id})
    except Exception as e:
        # 데이터베이스 오류 또는 기타 예상치 못한 오류
        raise ValueError(f"{str(e)}")
