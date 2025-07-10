from flask import Blueprint, request, jsonify, current_app, make_response, redirect
from app.services.user_service import sign_up_user, log_in_user

user_bp = Blueprint("user", __name__)


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


@user_bp.route("/log-in", methods=["POST"])
def log_in():
    """
    로그인 요청을 처리하는 라우트 핸들러입니다.
    - 이메일과 비밀번호를 받아 로그인 처리
    - 로그인 성공 시 토큰을 생성하여 쿠키에 저장
    """

    email = request.form["email_give"]
    password = request.form["password_give"]

    success, token, message = log_in_user(email, password)

    # jwt 토큰
    if not success:
        return jsonify({"success": False, "data": {}, "message": message})

    response = make_response(
        jsonify(
            {
                "success": True,
                "data": {},
                "message": "로그인 성공",
            }
        )
    )
    response.set_cookie("access_token", token, httponly=False)

    return response


@user_bp.route("/logout")
def logout():
    response = make_response(redirect("/login"))  # 로그아웃 후 로그인 페이지로 이동
    response.set_cookie("access_token", "", expires=0)
    return response
