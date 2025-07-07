from app import db

# from app.models.user_model import get_user_by_id, insert_user


def create_user(data):
    # 유효성 검사 (예: 이름 필수)
    if "name" not in data:
        raise ValueError("Name is required")

    # return insert_user(data)


# def get_user(user_id):
# return get_user_by_id(user_id)
