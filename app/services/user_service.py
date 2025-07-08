import bcrypt
from app.models.user_model import insert_user, is_email_exist


def create_user(data):
    # 유효성 검사 (예: 이름 필수)
    if "name" not in data:
        raise ValueError("Name is required")

    # return insert_user(data)


# def get_user(user_id):
# return get_user_by_id(user_id)


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

    if is_email_exist(email):
        return {"success": False, "data": {}, "message": "이미 존재하는 이메일입니다."}

    # 비밀번호 해싱
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt)

    insert_user({"nickname": nickname, "email": email, "password": hashed_pw.decode()})

    return {"success": True, "data": {}, "message": "회원가입이 완료되었습니다."}
