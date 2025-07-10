from flask import Blueprint, request, jsonify, current_app, render_template

from app.models.challenge_model import get_challenge_by_id
from app.services.auth_service import get_user_by_token

rendering_bp = Blueprint("rendering", __name__)


@rendering_bp.route("/", methods=["GET"])
def main():
    testuser = None
    # testuser="aaa"

    return render_template("main_page.html", current_user_nickname=testuser)


@rendering_bp.route("/register", methods=["GET"])
def signup():
    return render_template("signup_page.html")


@rendering_bp.route("/mypage", methods=["GET"])
def mypage():
    # 유저 정보를 얻어와야 함 (token?)
    # 토큰을 넘기고 mypage.html에서 서버로 private challenge 정보 요청

    return render_template("mypage.html")


@rendering_bp.route("/challenge/<challenge_id>", methods=["GET"])
def render_challenge_detail(challenge_id):
    try:
        token = request.cookies.get("access_token")
        # 서비스 함수를 통해 챌린지 정보 조회
        challenge_info = get_challenge_by_id(challenge_id)
        if not challenge_info:
            return (
                render_template(
                    "challenge_detail_page.html", error="존재하지 않는 챌린지입니다."
                ),
                404,
            )

        # 현재 사용자 정보 (세션에서 가져오거나 토큰에서 추출)
        current_user = get_user_by_token(token)
        start_date_str = challenge_info["start_date"].strftime("%Y-%m-%d")
        end_date_str = challenge_info["end_date"].strftime("%Y-%m-%d")

        return render_template(
            "challenge_detail_page.html",
            challenge_id=challenge_id,
            challenge_name=challenge_info["title"],
            challenge_count=challenge_info["challenge_count"],
            start_date=start_date_str,
            end_date=end_date_str,
            current_user_nickname=current_user["nickname"] if current_user else None,
        )
    except Exception as e:
        print(str(e))
        return render_template("main_page.html", error="챌린지를 찾을 수 없습니다.")
