from flask import Blueprint, jsonify, request
from app.services.record_service import (
    post_record_service,
    get_all_record_service,
    get_one_record_by_id_service,
)

from bson.json_util import dumps

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


@record_bp.route("/<record_id>", methods=["GET"])
def get_one_record_by_id(record_id):
    try:
        # user_id = "686cd2b4fce5f626c62cad5a"
        result = get_one_record_by_id_service(record_id)
        return jsonify(
            {
                "success": True,
                "data": result,
                "message": "레코드 조회 성공",
            }
        )

    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@record_bp.route("/", methods=["GET"])
def get_all_record():
    try:
        challenge_id = request.args.get("challenge_id")
        # user_id = "686cd2b4fce5f626c62cad5a"
        print(challenge_id)

        result = get_all_record_service(challenge_id)
        return jsonify(
            {
                "success": True,
                "data": result,
                "message": "레코드 등록 성공",
            }
        )

    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
