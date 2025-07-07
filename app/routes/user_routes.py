from flask import Blueprint, request, jsonify
from app import db

user_bp = Blueprint("user", __name__)


@user_bp.route("/", methods=["GET"])
def list_users():
    users = db["users"].find()
    result = [{"id": str(u["_id"]), "name": u["name"]} for u in users]
    return jsonify(result)


@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.json
    db["users"].insert_one({"name": data.get("name")})
    return jsonify({"success": True}), 201
