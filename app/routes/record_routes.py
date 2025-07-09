from flask import Blueprint, jsonify, request
from app.services.record_service import post_record_service

record_bp = Blueprint("record", __name__)


@record_bp.route("/", methods=["POST"])
def post_record():
    try:
        record_data = request.get_json()
        challenge_id = request.args.get("challenge_id")
        user_id = "686cd2b4fce5f626c62cad5a"

        result = post_record_service(record_data, challenge_id, user_id)
        return jsonify(
            {
                "success": True,
                "data": {
                    "record_id": str(result.inserted_id),
                },
                "message": "레코드 등록 성공",
            }
        )

    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400

    except Exception as e:
        return jsonify({"success": False, "error": "Internal server error"}), 500
