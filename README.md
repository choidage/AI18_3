# AI18_3 - 넷플릭스 영화 추천 시스템

AI18기 3차 Project - Streamlit 기반 영화 추천 웹 애플리케이션

## 🎬 프로젝트 소개

넷플릭스 스타일의 다크 테마를 적용한 영화 추천 시스템입니다. 사용자의 선호도(장르, 연도, 평점)를 기반으로 맞춤형 영화를 추천합니다.

## ✨ 주요 기능

- 🎯 **맞춤형 추천**: 사용자 선호도 기반 영화 추천
- 🎨 **넷플릭스 스타일 UI**: 다크 테마와 레드 컬러를 활용한 모던한 디자인
- 📊 **통계 대시보드**: 장르별, 연도별 영화 분포 시각화
- 🔥 **인기 영화**: 평점 기반 TOP 10 영화 표시
- 🎭 **다양한 장르**: 액션, 드라마, 로맨스, 코미디, SF 등

## 🚀 실행 방법

### 1. 가상환경 설정 (Conda)

```bash
# Conda 환경 활성화
conda activate py3_11_9

# 또는 직접 Python 경로 사용
D:\Anaconda3\envs\py3_11_9\python.exe
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. Streamlit 앱 실행

```bash
streamlit run streamlit_app.py
```

또는 conda 환경의 Python으로 직접 실행:

```bash
D:\Anaconda3\envs\py3_11_9\Scripts\streamlit.exe run streamlit_app.py
```

### 4. 브라우저에서 확인

자동으로 브라우저가 열리며 `http://localhost:8501`에서 앱을 확인할 수 있습니다.

## 📁 프로젝트 구조

```
AI18_3/
├── streamlit_app.py      # Streamlit 메인 애플리케이션
├── app.py                # Flask 애플리케이션 (참고용)
├── requirements.txt      # Python 패키지 목록
├── .gitignore           # Git 제외 파일 목록
└── README.md            # 프로젝트 설명서
```

## 🛠️ 기술 스택

- **Python 3.11.9**
- **Streamlit**: 웹 애플리케이션 프레임워크
- **Pandas**: 데이터 처리 및 분석
- **NumPy**: 수치 연산

## 📝 사용 방법

1. 사이드바에서 선호하는 장르 선택
2. 선호하는 연도 범위 설정
3. 최소 평점 설정
4. 맞춤형 추천 영화 확인
5. 통계 대시보드에서 영화 분포 확인

## 🎯 추천 알고리즘

- 평점 기반 정렬
- 사용자 선호도 필터링 (장르, 연도, 평점)
- 상위 5개 영화 추천

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.
