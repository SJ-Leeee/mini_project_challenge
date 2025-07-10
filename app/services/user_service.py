from flask import current_app
from app.models.user_model import insert_user, is_email_exist
from app.services.auth_service import create_access_token
from app.utils.validation_utils import is_valid_email, is_valid_password


import bcrypt
import jwt


def create_user(data):
    # 유효성 검사 (예: 이름 필수)
    if "name" not in data:
        raise ValueError("Name is required")

    # return insert_user(data)


# def get_user(user_id):
# return get_user_by_id(user_id)


# TODO: email, password 유효성 검사 로직 추가 필요
def sign_up_user(data):
    """
    회원가입 요청 데이터를 받아 유저 등록을 처리합니다.

    Parameters:
        data (dict): nickname, email, password를 포함한 요청 데이터.

    Returns:
        dict: 회원가입 처리 결과 메시지를 포함한 응답 객체.
    """
    nickname = data.get("nickname_give")
    email = data.get("email_give")
    password = data.get("password_give")

    if not is_valid_email(email):
        return {
            "success": False,
            "data": {},
            "message": "이메일 형식이 올바르지 않습니다.",
        }
    if not is_valid_password(password):
        return {
            "success": False,
            "data": {},
            "message": "비밀번호 형식이 올바르지 않습니다.",
        }

    if is_email_exist(email):
        return {"success": False, "data": {}, "message": "이미 존재하는 이메일입니다."}

    # 비밀번호 해싱
    if isinstance(password, str):
        password = password.encode()

    hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

    insert_user({"nickname": nickname, "email": email, "password": hashed_pw.decode()})

    return {"success": True, "data": {}, "message": "회원가입이 완료되었습니다."}


def log_in_user(email, password):
    """
    이메일과 비밀번호로 사용자를 인증하고, 성공 시 access token 반환

    Parameters:
        email (str): 로그인 요청의 이메일
        password (str): 로그인 요청의 비밀번호

    Returns:
        tuple:
            - success (bool): 로그인 성공 여부
            - token (str or None): 로그인 성공 시 JWT access token, 실패 시 None
            - message (str): 처리 결과 메시지 (성공/실패 이유)
    """

    if not is_valid_email(email):
        return (
            False,
            "",
            "이메일 형식이 올바르지 않습니다.",
        )
    if not is_valid_password(password):
        (
            False,
            "",
            "비밀번호 형식이 올바르지 않습니다.",
        )

    db = current_app.config["DB"]
    user = db["users"].find_one({"email": email})

    if not user:
        return False, None, "존재하지 않는 사용자입니다."

    # user["password"] 주의 필요.
    # DB에 저장된 password가 문자열인지, 바이트인지 확인이 필요합니다.
    # 바이트 형태일 경우 user["password"].encode()는 실패합니다.
    stored_pw = user["password"]
    if isinstance(stored_pw, str):
        stored_pw = stored_pw.encode()

    if not bcrypt.checkpw(password.encode(), stored_pw):
        return False, None, "비밀번호가 일치하지 않습니다."

    token = create_access_token(user["_id"])

    return True, token, "로그인 성공"
