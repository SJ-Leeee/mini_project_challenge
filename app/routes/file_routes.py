from flask import Blueprint, request, jsonify

from app.utils.s3_func import upload_file_to_s3, delete_s3_file_by_url

file_bp = Blueprint("file", __name__)


@file_bp.route("/", methods=["POST"])
def upload():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "파일이 없습니다."}), 400

        filename = file.filename
        url = upload_file_to_s3(file, filename)

        return jsonify({"success": True, "message": "업로드 성공", "url": url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@file_bp.route("/", methods=["DELETE"])
def delete_image():
    file_url = request.args.get("file_url")
    if not file_url:
        return jsonify({"error": "file_url required"}), 400

    try:
        delete_file_from_s3(file_url)

        return jsonify({"message": "삭제 성공"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
