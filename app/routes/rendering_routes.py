from flask import Blueprint, request, jsonify, current_app, render_template
from jwt import decode, ExpiredSignatureError
from app.services.challenge_service import get_challenges_service
from app.services.auth_service import auth_token
from datetime import datetime

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


@rendering_bp.route("/main_modal", methods=["GET"])
def main_modal():
    """검색 모달 페이지"""
    # URL 파라미터에서 기본값 가져오기 (선택사항)
    search_query = request.args.get("query", "")
    topic = request.args.get("topic", "all")
    sort = request.args.get("sort", "recent")
    ascending = request.args.get("ascending", "false")

    return render_template(
        "main_modal.html",
        search_query=search_query,
        topic=topic,
        sort=sort,
        ascending=ascending == "false",
    )


@rendering_bp.route("/main_search", methods=["GET", "POST"])
def main_search():
    search_query = request.form.get("query", "").strip()
    topic = request.form.get("topic", "all")
    sort = request.form.get("sort", "recent")
    ascending = request.form.get("ascending", "false")

    print(search_query, topic, sort, ascending)

    # 유효한 토픽 값인지 확인
    valid_topics = ["all", "exercise", "study", "life"]
    if topic not in valid_topics:
        topic = "all"

    # 유효한 정렬 값인지 확인
    valid_sorts = ["recent", "popular"]
    if sort not in valid_sorts:
        sort = "recent"

    # 검색 로직 수행
    search_results = perform_search(search_query, topic, sort, ascending)
    print(search_results)

    results = []
    for item in search_results:
        start_date = item["start_date"]
        end_date = item["end_date"]

        days_from_start = (datetime.now() - start_date).days
        days_until_end = (end_date - datetime.now()).days

        results.append(
            {
                "title": item["title"],
                "likes": item["like_count"],
                "days_from_start": days_from_start,
                "days_until_end": days_until_end,
            }
        )

    return render_template(
        "main_search_result.html",
        results=results,
        query=search_query,
        topic=topic,
        sort=sort,
        ascending=ascending,
    )


def perform_search(query, topic, sort, ascending, private = True, user_id = None):
    print("perform_search()")
    # public challenge만 취합
    # sort 값에 따라 최신순, 좋아요 순 정렬
    sort = 1 if sort == "recent" else 0
    print(private)
    results = get_challenges_service(sort, private, user_id)

    # print(results)

    # topic과 일치하는 challenge만
    if topic != "all":
        if topic == "health":
            topic = 0
        elif topic == "study":
            topic = 1
        elif topic == "life":
            topic = 2

        results = [
            result
            for result in results
            if result.get("topic") is not None and result.get("topic") == topic
        ]

    # ascending에 따라 오름차순, 내림차순 정렬
    if ascending == "true":
        results = results[::-1]

    # query로 challenge title을 검색
    # query string이 없으면 생략
    if query and query.strip():
        query_lower = query.lower()
        results = [
            result
            for result in results
            if result.get("title") and query_lower in result.get("title").lower()
        ]

    # print(results)
    return results


@rendering_bp.route("/mypage_modal", methods=["GET"])
def mypage_modal():
    search_query = request.form.get("query", "").strip()
    topic = request.form.get("topic", "all")
    sort = request.form.get("sort", "recent")
    ascending = request.form.get("ascending", "false")
    private = request.form.get("private", "false")

    return render_template(
        "mypage_modal.html",
        search_query=search_query,
        topic=topic,
        sort=sort,
        ascending=ascending == "false",
        private=private == "false",
    )


@rendering_bp.route("/mypage_search", methods=["GET", "POST"])
def mypage_search():
    token = request.cookies.get("access_token")
    is_valid, result = auth_token(token)
    if not is_valid:
        render_template("main_page.html", mesage=result)

    print(result)

    user_id = result

    search_query = request.form.get("query", "").strip()
    topic = request.form.get("topic", "all")
    sort = request.form.get("sort", "recent")
    ascending = request.form.get("ascending", "false")
    private = request.form.get("private", "false")

    print(search_query, topic, sort, ascending, private)

    # 유효한 토픽 값인지 확인
    valid_topics = ["all", "exercise", "study", "life"]
    if topic not in valid_topics:
        topic = "all"

    # 유효한 정렬 값인지 확인
    valid_sorts = ["recent", "popular"]
    if sort not in valid_sorts:
        sort = "recent"

    # 검색 로직 수행
    if private == 'true':
        search_results = perform_search(search_query, topic, sort, ascending, False, user_id)
    else:
        search_results = perform_search(search_query, topic, sort, ascending)
    print(search_results)

    results = []
    for item in search_results:
        start_date = item["start_date"]
        end_date = item["end_date"]

        days_from_start = (datetime.now() - start_date).days
        days_until_end = (end_date - datetime.now()).days

        results.append(
            {
                "title": item["title"],
                "likes": item["like_count"],
                "days_from_start": days_from_start,
                "days_until_end": days_until_end,
            }
        )

    return render_template(
        "main_search_result.html",
        results=results,
        query=search_query,
        topic=topic,
        sort=sort,
        ascending=ascending,
    )
