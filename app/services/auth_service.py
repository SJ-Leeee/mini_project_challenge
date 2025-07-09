from flask import current_app
from datetime import datetime, timedelta

import jwt

# JWT 관련 상수 설정
SECRET_KEY = "HYEONGILSEUNGJUNJIHOON"
EXPIRE_TIME = 15  # access token의 만료 기간 (분)

def create_access_token(id):
    """
    사용자 ID(ObjectId)를 받아 access token(JWT)을 생성하는 함수

    Parameter:
        id (ObjectId): mongoDB에서 user를 삽입 시 자동으로 생성되는 ObjectId
    """

    payload = {
        "_id": str(id),  # ObjectId는 str로 변환.
        "exp": datetime.now() + timedelta(minutes=EXPIRE_TIME),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def auth_token(token):
    """
    전달된 JWT access token의 유효성을 검증하고,
    유효하면 payload에 포함된 _id를 반환한다.

    Parameters:
        token (str): 클라이언트로부터 전달받은 access token

    Returns:
        tuple:
            - is_valid (bool): 유효 여부
            - _id_or_message (str): _id 또는 에러 메시지
    """

    if not token:
        return False, "토큰이 없습니다."
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True, payload["_id"]
    except jwt.ExpiredSignatureError:
        return False, "토큰이 만료되었습니다."
    except jwt.InvalidTokenError:
        return False, "유효하지 않은 토큰입니다."