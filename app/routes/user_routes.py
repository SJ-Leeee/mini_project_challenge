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

@user_bp.route("/sign-up", method=["POST"])
def sign_up():
    data = request.form
    result = sign_up_user(data)
    return jsonify(result)
