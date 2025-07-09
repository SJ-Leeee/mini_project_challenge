from app.models.record_model import (
    get_challenge_by_id_with_userId,
    post_record_model,
    get_record_by_challenge_id_with_today,
    get_all_record_model,
    get_one_record_by_id_model,
)


def post_record_service(record_data, challenge_id, user_id):
    try:
        oneline_diary = record_data["oneline_diary"]
        # photo_data = record_data["photo_data"]
        if not isinstance(oneline_diary, str) and len(oneline_diary) > 40:
            raise ValueError("oneline_diary must exist and less than 40 character")
        if not user_id or not challenge_id:
            raise ValueError("must have challenge or user")

        photo_url = None
        # if photo_data:
        #     photo_url = get_url_from_S3(photo_data)
        challenge = get_challenge_by_id_with_userId(challenge_id, user_id)
        if not challenge:
            raise ValueError("not exist challenge")

        exsist_record = get_record_by_challenge_id_with_today(challenge["_id"])
        if exsist_record:
            raise ValueError("이미 레코드가 존재합니다. 삭제하고 다시 만들어주세요.")

        result = post_record_model(oneline_diary, photo_url, challenge)
        return result
    except Exception as e:
        # 데이터베이스 오류 또는 기타 예상치 못한 오류
        raise ValueError(f"{str(e)}")


def get_one_record_by_id_service(record_id):
    record = get_one_record_by_id_model(record_id)
    if not record:
        raise ValueError("record is not exist")
    return record


def get_all_record_service(challenge_id):
    records = get_all_record_model(challenge_id)
    if not records:
        raise ValueError("record is not exist")
    return records


# def get_url_from_S3(data):
