"""
간단한 Flask 웹 애플리케이션
GitHub 실습을 위한 기본 예제 파일
"""
from flask import Flask

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# 루트 경로에 대한 라우트 정의
@app.route('/')
def hello():
    """메인 페이지를 반환하는 함수"""
    return '<h1>Hello, GitHub!</h1><p>이것은 GitHub 실습을 위한 앱입니다.</p>'

# /about 경로에 대한 라우트 정의
@app.route('/about')
def about():
    """소개 페이지를 반환하는 함수"""
    return '<h1>About</h1><p>이 프로젝트는 GitHub 실습을 위한 것입니다.</p>'

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

