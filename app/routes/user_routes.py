from flask import Blueprint, request, jsonify, current_app
from app.services.user_service import sign_up_user

user_bp = Blueprint("user", __name__)


@user_bp.route("/", methods=["GET"])
def list_users():
    db = current_app.config["DB"]
    print(db)
    db["users"].insert_one({"name": "test"})
    return "hi"


# def list_users():
#     result = [{"id": str(u["_id"]), "name": u["name"]} for u in users]
#     return jsonify(result)


# @user_bp.route("/", methods=["POST"])
# def create_user():
#     data = request.json
#     db["users"].insert_one({"name": data.get("name")})
#     return jsonify({"success": True}), 201

@user_bp.route("/sign-up", methods=["POST"])
def sign_up():
    """
    클라이언트로부터 전달받은 회원가입 요청을 처리합니다.

    Returns: 
        JSON 응답: 회원가입 성공/실패 여부와 메시지
    """
    data = request.form
    result = sign_up_user(data)
    return jsonify(result)
