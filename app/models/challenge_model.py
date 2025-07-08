from flask import current_app, jsonify
from bson import ObjectId
from enum import Enum
from datetime import datetime, timedelta


class ChallengeSortType(Enum):
    LIKE = 0
    RECENT = 1
    COMMENT = 2


def get_challenges_model(sort_type):
    sort = ChallengeSortType(sort_type)
    db = current_app.config["DB"]
    if sort == ChallengeSortType.LIKE:
        db["challenges"].find()


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
            "user_id": user_id,
            "start_date": today,  # 2025-07-08
            "end_date": end_date,  # 2025-08-01
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        result = challenge_collection.insert_one(challenge)
        return {
            "success": True,
            "data": {
                "challenge_id": str(result.inserted_id),
            },
            "message": "챌린지 등록이 되었습니다.",
        }

    except Exception as e:
        # 데이터베이스 오류 또는 기타 예상치 못한 오류
        raise ValueError(f"{str(e)}")
