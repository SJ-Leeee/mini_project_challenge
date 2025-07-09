from bson import ObjectId
from flask import Blueprint, request, jsonify, current_app, render_template
from datetime import datetime, timedelta, date
from app.services.auth_service import auth_token
from app.services.challenge_service import (
    get_challenges_service,
)
from app.services.record_service import (
    get_all_record_by_challenge_id,
)

rendering_bp = Blueprint("rendering", __name__)

@rendering_bp.route("/", methods=["GET"])
def main():
    token = request.cookies.get("access_token")
    is_valid, _id = auth_token(token)

    current_user = None

    if is_valid:
        db = current_app.config["DB"]
        user = db["users"].find_one({"_id":ObjectId(_id)})

        current_user = user["nickname"]
    
    data = get_challenges_service(0, True)
    results = []

    for challenge in data:
        records_data = []

        records = get_all_record_by_challenge_id(challenge["_id"])

        for record in records:
            month = int(record["created_date"][:2])
            day = int(record["created_date"][2:])

            record_date = date(datetime.now().year, month, day)

            if (7 > (datetime.now().date() - record_date).days):
                records_data.append((datetime.now().date() - record_date).days)

        print(records_data)
        results.append({
            "id": challenge['_id'],
            "public": challenge['is_public'],
            "title": challenge['title'],
            "likes": challenge['like_count'],
            "days_from_start": (datetime.now() - challenge['start_date']).days,
            "days_until_end": (challenge['end_date'] - datetime.now()).days,
            "records_data": records_data.sort()
        })
        
    return render_template('main_page.html', current_user_nickname=current_user, card_datas=results)

@rendering_bp.route("/register", methods=["GET"])
def signup():
    return render_template('signup_page.html')

@rendering_bp.route("/mypage", methods=["GET"])
def mypage():
    data = get_challenges_service(0, True)
    results = []

    for challenge in data:
        records_data = []

        records = get_all_record_service(challenge["_id"])

        for record in records:
            month = int(record["created_date"][:2])
            day = int(record["created_date"][2:])

            record_date = date(datetime.now().year, month, day)

            if (7 > (datetime.now().date() - record_date).days):
                records_data.append((datetime.now().date() - record_date).days)

        print(records_data)
        results.append({
            "id": challenge['_id'],
            "public": challenge['is_public'],
            "title": challenge['title'],
            "likes": challenge['like_count'],
            "days_from_start": (datetime.now() - challenge['start_date']).days,
            "days_until_end": (challenge['end_date'] - datetime.now()).days,
            "records_data": records_data.sort()
        })

    return render_template('mypage.html')