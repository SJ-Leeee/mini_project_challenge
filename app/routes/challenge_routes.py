from flask import Blueprint, request, jsonify
from app.services.challenge_service import (
    get_challenges_service,
    create_challenge_service,
    like_challenge_service,
)
from app.utils.enum.ChallengeSortTypeEnum import ChallengeSortType

challenge_bp = Blueprint("challenge", __name__)


# 퍼블릭 챌린지 조회
# localhost:5000/api/challenge/public?sort=2
@challenge_bp.route("/public", methods=["GET"])
def get_public_challenges():
    sort = request.args.get("sort", "0")  # 기본값 지정 = Optional
    is_public = True
    try:
        # enum 확인
        ChallengeSortType(int(sort))
        # 서비스 호출
        data = get_challenges_service(int(sort), is_public)
        return data
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# 프라이빗 챌린지 조회
# localhost:5000/api/challenge/private?sort=2
@challenge_bp.route("/private", methods=["GET"])
def get_private_challenges():
    sort = request.args.get("sort", "1")  # 기본값 지정 = Optional
    is_public = False
    # user_id = get_current_user()
    user_id = 1

    # 이부분에서 user_id없으면 Error
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401

    try:
        # enumType 확인
        ChallengeSortType(int(sort))
        # 서비스 호출
        data = get_challenges_service(int(sort), is_public, user_id)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# 챌린지 등록 API
# localhost:5000/api/challenge
@challenge_bp.route("/", methods=["POST"])
def post_challenge():
    # 기본적인 요청 형식 검증
    challenge_data = request.get_json()
    if not challenge_data:
        return jsonify({"error": "No data provided"}), 400

    # user_id = get_current_user()
    user_id = 1
    # 이부분에서 user_id없으면 Error
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    try:
        # 서비스 호출
        result = create_challenge_service(challenge_data, user_id)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# localhost:5000/api/challenge/like
@challenge_bp.route("/like", methods=["PATCH"])
def like_challenge():
    challenge_id = request.args.get("challenge_id")  # 기본값 지정 = Optional
    # user_id = get_current_user()
    user_id = "686cd2b4fce5f626c62cad5a"
    # 이부분에서 user_id없으면 Error
    if not user_id or not challenge_id:
        return jsonify({"error": "Authentication or C22hallengeID required"}), 401
    try:
        # 서비스 호출
        result = like_challenge_service(user_id, challenge_id)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
