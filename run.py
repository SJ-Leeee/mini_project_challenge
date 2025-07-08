# run.py

from app import create_app

app = create_app()  # 앱 생성

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # 여기서 실행
# 테스트
