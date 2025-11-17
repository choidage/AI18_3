"""
넷플릭스 기반 선호 영화 추천 시스템
Streamlit을 사용한 인터랙티브 웹 애플리케이션
"""
import streamlit as st
import pandas as pd
import random
from typing import List, Dict

# 페이지 설정 - 밝은 테마
st.set_page_config(
    page_title="영화 추천 시스템",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링 - 밝은 테마 (흰색/회색 배경, 진한 글자)
st.markdown("""
<style>
    /* 메인 배경색 - 흰색/회색 */
    .stApp {
        background-color: #f5f5f5;
        color: #1a1a1a;
    }
    
    /* 헤더 스타일 */
    h1 {
        color: #3d2817 !important;  /* 진한 갈색 */
        font-weight: bold;
        text-align: center;
        padding: 20px 0;
    }
    
    h2 {
        color: #2c2c2c !important;  /* 진한 검정 */
        font-weight: bold;
        margin-top: 30px;
    }
    
    h3 {
        color: #2c2c2c !important;  /* 진한 검정 */
    }
    
    h4 {
        color: #3d2817 !important;  /* 진한 갈색 */
    }
    
    /* 카드 스타일 */
    .movie-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 15px;
        margin: 10px;
        transition: transform 0.2s;
        border: 1px solid #d0d0d0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .movie-card:hover {
        transform: scale(1.05);
        border-color: #8b6f47;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .movie-card h4 {
        color: #3d2817 !important;
        margin-bottom: 10px;
    }
    
    .movie-card p {
        color: #2c2c2c !important;
        margin: 5px 0;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background-color: #8b6f47;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #6b5637;
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background-color: #ffffff;
    }
    
    /* 텍스트 색상 */
    .stMarkdown {
        color: #2c2c2c;
    }
    
    /* 일반 텍스트 */
    p {
        color: #2c2c2c !important;
    }
    
    /* 구분선 */
    hr {
        border-color: #d0d0d0;
    }
    
    /* 메트릭 스타일 */
    [data-testid="stMetricValue"] {
        color: #3d2817 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #2c2c2c !important;
    }
</style>
""", unsafe_allow_html=True)

# 영화 데이터베이스 (예제 데이터)
@st.cache_data
def load_movies() -> pd.DataFrame:
    """영화 데이터를 로드하는 함수"""
    movies_data = {
        'title': [
            '기생충', '올드보이', '신과함께', '극한직업', '명량',
            '베테랑', '암살', '국제시장', '도둑들', '해운대',
            '인터스텔라', '인셉션', '다크나이트', '어벤져스', '어벤져스: 엔드게임',
            '토르: 라그나로크', '아이언맨', '스파이더맨', '블랙팬서', '가디언즈 오브 갤럭시',
            '라라랜드', '위대한 쇼맨', '보헤미안 랩소디', '어바웃 타임', '노트북',
            '타이타닉', '인터뷰', '어바웃 타임', '러브 액츄얼리', '노팅힐'
        ],
        'genre': [
            '드라마', '스릴러', '판타지', '코미디', '액션',
            '액션', '액션', '드라마', '액션', '드라마',
            'SF', 'SF', '액션', '액션', '액션',
            '액션', '액션', '액션', '액션', '액션',
            '로맨스', '뮤지컬', '드라마', '로맨스', '로맨스',
            '로맨스', '코미디', '로맨스', '로맨스', '로맨스'
        ],
        'year': [
            2019, 2003, 2017, 2019, 2014,
            2015, 2015, 2014, 2012, 2009,
            2014, 2010, 2008, 2012, 2019,
            2017, 2008, 2017, 2018, 2014,
            2016, 2017, 2018, 2013, 2004,
            1997, 2014, 2013, 2003, 1999
        ],
        'rating': [
            9.1, 9.0, 7.3, 8.1, 8.1,
            8.1, 8.1, 8.4, 7.2, 6.4,
            9.0, 9.2, 9.0, 8.0, 9.1,
            8.4, 8.4, 8.4, 7.3, 8.0,
            8.4, 8.2, 9.1, 8.1, 8.5,
            8.4, 7.1, 8.1, 7.6, 7.7
        ],
        'description': [
            '반지하에 사는 기택 가족과 고급 주택에 사는 박 사장 가족의 이야기',
            '15년간 감금당한 남자가 복수를 위해 나서는 스릴러',
            '저승차사와 함께 저승으로 가는 49일간의 여정',
            '마약 조직을 잡기 위해 치킨집을 운영하는 형사들의 이야기',
            '임진왜란 당시 이순신 장군의 명량 해전',
            '한 형사와 재벌 3세의 대결',
            '일제강점기 독립운동가들의 암살 작전',
            '1950년대부터 현재까지 한 가족의 이야기',
            '10명의 도둑들이 다이아몬드를 훔치는 작전',
            '2004년 인도양 쓰나미를 소재로 한 재난 영화',
            '인류를 구하기 위한 우주 여행',
            '꿈 속으로 들어가는 도둑들의 이야기',
            '배트맨과 조커의 대결',
            '어벤져스 팀의 첫 번째 모임',
            '타노스와의 최종 결전',
            '토르의 새로운 모험',
            '토니 스타크의 아이언맨 탄생',
            '피터 파커의 스파이더맨 이야기',
            '와칸다의 새로운 왕',
            '우주의 수호자들의 모험',
            '재즈 피아니스트와 배우의 로맨스',
            '서커스 쇼맨의 성공 스토리',
            '퀸의 프레디 머큐리 이야기',
            '시간 여행이 가능한 남자의 로맨스',
            '노트북에 적힌 사랑 이야기',
            '타이타닉 호에서 만난 두 사람의 사랑',
            '북한에서 온 기자와의 인터뷰',
            '시간 여행이 가능한 남자의 로맨스',
            '크리스마스 이브의 런던 이야기',
            '책방 주인과 유명 배우의 로맨스'
        ]
    }
    return pd.DataFrame(movies_data)

def get_user_preferences() -> Dict:
    """사용자 선호도를 수집하는 함수"""
    st.sidebar.header("🎯 선호도 설정")
    
    # 선호 장르 선택
    genres = ['전체', '액션', '드라마', '로맨스', '코미디', 'SF', '스릴러', '판타지', '뮤지컬']
    selected_genre = st.sidebar.selectbox("선호하는 장르", genres)
    
    # 선호 연도 범위
    year_range = st.sidebar.slider("선호하는 연도 범위", 1990, 2020, (2000, 2020))
    
    # 최소 평점
    min_rating = st.sidebar.slider("최소 평점", 6.0, 10.0, 7.0, 0.1)
    
    return {
        'genre': selected_genre,
        'year_range': year_range,
        'min_rating': min_rating
    }

def filter_movies(movies_df: pd.DataFrame, preferences: Dict) -> pd.DataFrame:
    """선호도에 따라 영화를 필터링하는 함수"""
    filtered = movies_df.copy()
    
    # 장르 필터링
    if preferences['genre'] != '전체':
        filtered = filtered[filtered['genre'] == preferences['genre']]
    
    # 연도 필터링
    year_min, year_max = preferences['year_range']
    filtered = filtered[(filtered['year'] >= year_min) & (filtered['year'] <= year_max)]
    
    # 평점 필터링
    filtered = filtered[filtered['rating'] >= preferences['min_rating']]
    
    return filtered

def recommend_movies(movies_df: pd.DataFrame, num_recommendations: int = 5) -> List[Dict]:
    """영화를 추천하는 함수 (평점 기반)"""
    # 평점이 높은 순으로 정렬
    sorted_movies = movies_df.sort_values('rating', ascending=False)
    
    # 상위 영화 선택
    top_movies = sorted_movies.head(num_recommendations)
    
    recommendations = []
    for _, movie in top_movies.iterrows():
        recommendations.append({
            'title': movie['title'],
            'genre': movie['genre'],
            'year': movie['year'],
            'rating': movie['rating'],
            'description': movie['description']
        })
    
    return recommendations

def display_movie_card(movie: Dict):
    """영화 카드를 표시하는 함수"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # 영화 포스터 대신 이모지 사용
        st.markdown(f"### 🎬")
    
    with col2:
        st.markdown(f"**{movie['title']}** ({movie['year']})")
        st.markdown(f"⭐ 평점: {movie['rating']}/10 | 장르: {movie['genre']}")
        st.markdown(f"📝 {movie['description']}")

def main():
    """메인 함수"""
    # 헤더
    st.title("🎬 영화 추천 시스템")
    st.markdown("---")
    
    # 영화 데이터 로드
    movies_df = load_movies()
    
    # 사용자 선호도 수집
    preferences = get_user_preferences()
    
    # 필터링된 영화
    filtered_movies = filter_movies(movies_df, preferences)
    
    # 메인 컨텐츠 영역
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 맞춤 추천 영화")
        
        if len(filtered_movies) > 0:
            # 추천 영화 가져오기
            recommendations = recommend_movies(filtered_movies, num_recommendations=5)
            
            # 추천 영화 표시
            for i, movie in enumerate(recommendations, 1):
                with st.container():
                    st.markdown(f"### {i}. {movie['title']}")
                    col_a, col_b = st.columns([1, 2])
                    with col_a:
                        st.markdown(f"**연도:** {movie['year']}  \n**장르:** {movie['genre']}  \n**평점:** ⭐ {movie['rating']}/10")
                    with col_b:
                        st.markdown(f"**줄거리:** {movie['description']}")
                    st.markdown("---")
        else:
            st.warning("선호하신 조건에 맞는 영화가 없습니다. 조건을 변경해보세요!")
    
    with col2:
        st.header("📊 통계")
        st.metric("전체 영화 수", len(movies_df))
        st.metric("추천 영화 수", len(filtered_movies))
        
        # 장르별 분포
        st.subheader("장르별 분포")
        genre_counts = movies_df['genre'].value_counts()
        st.bar_chart(genre_counts)
        
        # 연도별 분포
        st.subheader("연도별 분포")
        year_counts = movies_df['year'].value_counts().sort_index()
        st.line_chart(year_counts)
    
    # 하단 섹션 - 인기 영화
    st.markdown("---")
    st.header("🔥 인기 영화 TOP 10")
    
    top_10 = movies_df.nlargest(10, 'rating')
    cols = st.columns(5)
    
    for idx, (_, movie) in enumerate(top_10.iterrows()):
        with cols[idx % 5]:
            st.markdown(f"""
            <div class="movie-card">
                <h4>{movie['title']}</h4>
                <p>⭐ {movie['rating']}/10</p>
                <p>{movie['year']}년</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

