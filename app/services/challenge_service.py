from datetime import datetime
from flask import jsonify
from app.models.challenge_model import get_challenges_model, post_challenges_model
from enum import Enum


class TopicType(Enum):
    HEALTH = 0
    STUDY = 1
    LIFE = 2


def get_challenges_service(sort_type):
    return get_challenges_model(sort_type)


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
