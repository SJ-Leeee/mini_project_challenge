## 📜 개발 컨밴션

✅ 전체 구조 예시 (폴더 구조)

<pre><code>my_flask_project/
├── run.py     # Flask 서버 실행 진입점
│
├── app/
│   ├── __init__.py     # Flask 앱 및 DB 초기화
│   ├── config/
│   │   ├── __init__.py
│   │   └── default.py      # 설정 파일 (DB URI 등)
│
│   ├── routes/     # API 연동
│   │   ├── __init__.py
│   │   ├── user_routes.py
│   │   └── post_routes.py
│
│   ├── services/   # 유효성 검증, 로직 분기처리
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── post_service.py
│
│   ├── models/     # DB처리만 담당(insert, find .. )
│   │   ├── __init__.py
│   │   ├── user_model.py
│   │   └── post_model.py
├── tests/
│   ├── __init__.py
│   ├── test_user.py
│   └── test_post.py
│
├── .env                             # 환경 변수 (DB URI 등)
├── .gitignore                       # venv, __pycache__, .env 등 제외
├── requirements.txt                 # 패키지 목록
└── README.md                        # 프로젝트 설명
</code></pre>

⸻

✅ 1. 변수 / 함수 / 파일명 네이밍 규칙

| 요소     | 컨벤션             | 예시                              |
| -------- | ------------------ | --------------------------------- |
| 변수명   | `snake_case`       | `user_name`, `product_id`         |
| 함수명   | `snake_case`       | `get_user_data()`, `save_order()` |
| 클래스명 | `PascalCase`       | `User`, `OrderService`            |
| 상수명   | `UPPER_SNAKE_CASE` | `MAX_LENGTH`, `DB_NAME`           |
| 파일명   | `snake_case.py`    | `routes.py`, `user_service.py`    |

---

✅ 2. Flask 라우팅 규칙
• GET, POST 등 명확히 분리
• RESTful 구조 지향

```@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
...

@app.route("/users", methods=["POST"])
def create_user():
...
```

---

✅ 3. 폴더/모듈 분리 기준

| 파일        | 역할                                          |
| ----------- | --------------------------------------------- |
| routes.py   | API 경로 및 HTTP 메서드 정의                  |
| services.py | 실제 비즈니스 로직 (DB insert, validation 등) |
| models.py   | MongoDB와의 인터페이스 (insert/find/update)   |
| utils.py    | 공통 함수, 포맷터 등                          |
| config.py   | DB, 환경변수 설정                             |

---

✅ 4. API 응답 포맷 (기본 컨벤션)

```
{
"success": true,
"data": { ... },
"message": "조회 성공"
}
```

• 모든 응답은 JSON

• success, data, message 필드를 통일하면 프론트에서도 예측 가능

---

## 📜 작업 컨벤션

✅ 파이썬 작업환경

`python -m venv venv` # 가상환경 생성(한번만 실행)

`source venv/bin/activate` # macOS/Linux
`.\venv\Scripts\activate` # Windows

✅ 작업이 끝난 후

`deactivate`

✅ 패키지 설치

`pip install requests flask` # flask는 예시
`pip freeze > requirements.txt` # 버전노트에 패키지 기록

✅ 깃허브 pull한 후 패키지 통일되게 설치

pip install -r requirements.txt

## 📜깃허브 컨밴션

### ✅ 1. 브랜치 전략

| 브랜치이름 | 용도                            |
| ---------- | ------------------------------- |
| main       | 운영/배포용 (절대 직접 작업 ❌) |
| dev        | 통합 개발 브랜치 (기능 merge)   |
| feature/\* | 기능 개발용 개인 브랜치         |

예시:

• feature/user-login-api

• feature/post-create

---

### ✅ 2. 작업 흐름

1. dev 브랜치 최신 상태로부터 시작

`git checkout dev`

`git pull origin dev`

2. 기능 브랜치 생성

`git checkout -b feature/user-login-api`

3. 작업 후 커밋

`git add .`

`git commit -m "feat: 사용자 로그인 API 추가"`

4. 푸시

`git push origin feature/user-login-api`

5. GitHub에서 PR(Pull Request) 생성 (base: dev)

6. 코드리뷰 후 머지 → 브랜치 삭제

---

### ✅ 3. 커밋 메시지 컨벤션

| 타입     | 설명                         |
| -------- | ---------------------------- |
| feat     | 기능 추가                    |
| fix      | 버그 수정                    |
| refactor | 리팩토링 (기능 변화 없음)    |
| docs     | 문서 수정                    |
| style    | 코드 스타일 수정 (공백 등)   |
| chore    | 설정, 패키지, 잡다한 작업 등 |

예시:

• feat: 게시글 등록 API 구현

• fix: 로그인 오류 수정

• refactor: user_service 분리

---

### ✅ 4. 머지 방식

• PR → 리뷰 → 머지

---

### ✅ 5. 충돌 해결

`git checkout feature/내-브랜치`

`git pull origin dev # dev 브랜치 최신 반영`

✅ 충돌 해결 후

`git add .`

`git commit -m "fix: 충돌 해결"`

`git push origin feature/내-브랜치`

---

### ✅ 6. 팀 규칙 요약

• 브랜치 전략: dev / feature/\* / main

• 커밋 타입: feat, fix, refactor, docs, style, test, chore

• PR은 dev 브랜치 대상으로 생성

• 머지 방식은 팀 내에서 Squash 또는 Merge commit으로 통일

• main 브랜치에는 직접 푸시 ❌

---
