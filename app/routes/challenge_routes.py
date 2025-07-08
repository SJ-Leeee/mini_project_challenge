from flask import Blueprint, request, jsonify, current_app
from app.services.challenge_service import (
    get_challenges_service,
    create_challenge_service,
)
from enum import Enum

challenge_bp = Blueprint("challenge", __name__)


# @challenge_bp.route("/", methods=["GET"])
# def list_users():
#     db = current_app.config["DB"]
#     print(db)
#     db["users"].insert_one({"name": "test"})
#     return "hi"


class ChallengeSortType(Enum):
    LIKE = 0
    RECENT = 1
    COMMENT = 2


"""
기본값 0 -> 좋아요 순
     1 -> 최신 순
     2 -> 챌린지 댓글 순
"""


@challenge_bp.route("/", methods=["GET"])
def get_challenges():
    sort = request.args.get("sort", "0")  # 기본값 지정 = Optional
    try:
        ChallengeSortType(int(sort))
    except (ValueError, KeyError):
        return jsonify({"success": False, "message": "Invalid sort type"}), 400

    get_challenges_service(int(sort))

    return "hi"


@challenge_bp.route("/", methods=["POST"])
def post_challenge():
    # 기본적인 요청 형식 검증
    challenge_data = request.get_json()
    if not challenge_data:
        return jsonify({"error": "No data provided"}), 400

    # user_id = get_current_user()
    user_id = 1
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    try:
        # 서비스 호출
        result = create_challenge_service(challenge_data, user_id)
        return result, 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @challenge_bp.route("/", methods=["GET"])
# def list_users():
#     db = current_app.config["DB"]
#     print(db)
#     db["users"].insert_one({"name": "test"})
#     return "hi"


# @challenge_bp.route("/", methods=["GET"])
# def list_users():
#     db = current_app.config["DB"]
#     print(db)
#     db["users"].insert_one({"name": "test"})
#     return "hi"


# @challenge_bp.route("/", methods=["GET"])
# def list_users():
#     db = current_app.config["DB"]
#     print(db)
#     db["users"].insert_one({"name": "test"})
#     return "hi"
