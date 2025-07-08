from app.models.challenge_model import (
    post_challenges_model,
    get_public_challenge_model,
    get_private_challenge_model,
)
from app.utils.TopicTypeEnum import TopicType


def get_challenges_service(sort_type, is_public, user_id=None):
    # private API 요청했는데 user_id 없으면 오류
    if is_public == False and user_id == None:
        raise ValueError("you must be login")
    # 퍼블릭 결과요청
    if is_public == True:
        result = get_public_challenge_model(sort_type)
    # 프라이빗 결과요청
    else:
        result = get_private_challenge_model(sort_type, user_id)
    return result


def create_challenge_service(challenge_data, user_id):
    validate_challenge_data(challenge_data)
    result = post_challenges_model(challenge_data, user_id)
    return result


def validate_challenge_data(post_challenge_data):
    required_fields = ["title", "topic", "challenge_count", "is_public"]

    for field in required_fields:
        if field not in post_challenge_data:
            raise ValueError(f"{field} is required")

    # 타입 검증
    try:
        # title 검증
        if (
            not isinstance(post_challenge_data["title"], str)
            or not post_challenge_data["title"].strip()
        ):
            raise ValueError("title must be a non-empty string")

        # topic 검증
        try:
            TopicType(int(post_challenge_data["topic"]))
        except ValueError:
            raise ValueError("Invalid topic value")

        # challenge_count 검증
        if (
            not isinstance(post_challenge_data["challenge_count"], int)
            or post_challenge_data["challenge_count"] <= 0
        ):
            raise ValueError("challenge_count must be a positive integer")

        # is_public 검증
        if not isinstance(post_challenge_data["is_public"], bool):
            raise ValueError("is_public must be a boolean")

    except Exception as e:
        raise ValueError("Invalid data format")
