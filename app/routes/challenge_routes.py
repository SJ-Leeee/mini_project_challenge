from flask import Blueprint, request, jsonify, current_app

challenge_bp = Blueprint("challenge", __name__)


@challenge_bp.route("/", methods=["GET"])
def list_users():
    db = current_app.config["DB"]
    print(db)
    db["users"].insert_one({"name": "test"})
    return "hi"
