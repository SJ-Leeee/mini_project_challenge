from flask import Blueprint, request, jsonify, current_app, render_template

rendering_bp = Blueprint("rendering", __name__)

@rendering_bp.route("/", methods=["GET"])
def main():
    testuser=None
    #testuser="aaa"

    return render_template('main_page.html', current_user_nickname=testuser)

@rendering_bp.route("/register", methods=["GET"])
def signup():
    return render_template('signup_page.html')

@rendering_bp.route("/mypage", methods=["GET"])
def mypage():
    # 유저 정보를 얻어와야 함 (token?)
    # 토큰을 넘기고 mypage.html에서 서버로 private challenge 정보 요청

    return render_template('mypage.html')