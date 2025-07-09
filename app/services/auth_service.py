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