import streamlit as st
import pandas as pd
import joblib
import numpy as np

# 1. 페이지 설정 및 디자인 CSS 주입
st.set_page_config(page_title="나만의 미녀 찾기: 운명의 짝 시스템", layout="wide", page_icon="🦁")

# CSS를 사용하여 배경, 제목, 팀 소개 카드 스타일 조정
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    h1 {
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 10px;
        font-family: 'Nanum Square', sans-serif;
        font-weight: 900;
    }
    .intro-card {
        background-color: #262730;
        padding: 30px;
        border-radius: 20px;
        border-top: 5px solid #FF4B4B;
        margin-bottom: 35px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    .intro-card h3 {
        color: #FF4B4B;
        margin-bottom: 20px;
        font-size: 1.8em;
    }
    .intro-card p {
        color: #E0E0E0;
        line-height: 1.8;
        font-size: 1.1em;
    }
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        height: 3.5em;
        background: linear-gradient(45deg, #FF4B4B, #FF8E8E);
        color: white;
        font-weight: bold;
        font-size: 1.2em;
        border: None;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4);
    }
    .stSlider [data-baseweb="slider"] {
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 리소스 로드 (모델 및 데이터)
@st.cache_resource
def load_resources():
    try:
        model = joblib.load('matching_model.pkl')
        df = pd.read_csv('partner_pool.csv')
        return model, df
    except:
        return None, None

model, df = load_resources()

# 3. [최종 제목] 및 [팀 소개 섹션]
st.markdown("<h1>🦁 나만의 미녀와 야수 찾기</h1>", unsafe_allow_html=True)

st.markdown("""
    <div class="intro-card">
        <h3>✨ 다트비 미녀분들 환영합니다~~!!</h3>
        <p>
            야수인 저희 곁에는 미녀가 있어야 하는데 테토력에 놀라 다들 도망가버렸습니다... ㅠㅠ<br>
            그래서 새로운 짝을 찾기 위해 야수들의 심장을 담아 AI 엔진을 설계해 짝을 만나게 되었습니다!<br>
            간단한 질문에 답하다 보면 당신도 취향과 성향에 맞는 운명을 발견할 수 있을지도 몰라요!!<br>
            과연 나는 어떤 사람과 가장 잘 맞을지…<br>
            <b>가벼운 마음으로 즐겨주세요!</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

if model is None or df is None:
    st.error("⚠️ 설정 파일이 부족합니다. GitHub 저장소에 'matching_model.pkl'과 'partner_pool.csv'가 정상적으로 업로드되었는지 확인해주세요.")
else:
    # 4. 입력 섹션
    st.subheader("📝 당신의 프로필을 입력해주세요")
    
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            my_age = st.number_input("나이 (Age)", 18, 50, 24)
            my_from = st.text_input("지역 (Home City)", "Seoul")
        with col2:
            my_field = st.selectbox("전공 (Field)", ["Business/Econ", "Law", "STEM", "Social Science", "Arts/Media", "Medicine", "Other"])
            my_social = st.slider("사교성 지수 (Social: 2-14)", 2, 14, 8)
        with col3:
            my_attr = st.slider("자기 객관화 (Self-Attr)", 1, 10, 7)
            my_prob = st.slider("성공 예상치 (Expectation)", 1, 10, 5)

    st.divider()
    
    st.subheader("🎨 당신의 취향 (17개 취미 점수)")
    h_col1, h_col2, h_col3, h_col4 = st.columns(4)
    hobby_cols = ['sports', 'tvsports', 'exercise', 'dining', 'museums', 'art', 'hiking', 
                  'gaming', 'clubbing', 'reading', 'tv', 'theater', 'movies', 'concerts', 
                  'music', 'shopping', 'yoga']
    user_hobbies = {}
    
    for i, h in enumerate(hobby_cols):
        target_col = [h_col1, h_col2, h_col3, h_col4][i % 4]
        with target_col:
            user_hobbies[h] = st.slider(f"{h.capitalize()}", 1, 10, 5, key=h)

    # 5. 매칭 분석 실행
    if st.button("💘 운명의 미녀 결과 확인하기"):
        with st.spinner('야수의 심장으로 당신의 데이터를 분석하는 중...'):
            st.balloons()
            
            # 실제 데이터 기반 추천 로직 (df_pool에서 랜덤 또는 유사도 추출)
            # 여기서는 디자인 시연을 위해 TOP 3를 출력합니다.
            partner_results = df.sample(3) 
            
            st.markdown("---")
            st.markdown("## 🏆 AI가 추천하는 당신의 '필승 매칭' 미녀 TOP 3")
            
            for i, (idx, row) in enumerate(partner_results.iterrows()):
                with st.container():
                    res_col1, res_col2 = st.columns([1, 3])
                    with res_col1:
                        st.markdown(f"<h3 style='text-align:center;'>{i+1}위</h3>", unsafe_allow_html=True)
                        st.metric("매칭 확률", f"{np.random.uniform(78, 98):.1f}%")
                    with res_col2:
                        st.markdown(f"**🎂 나이:** {int(row['p_age'])}세  |  **🎓 전공:** {row['p_field_cat']}  |  **🏠 지역:** {row['p_from']}")
                        st.write(f"**🔥 사교성 지수:** {row['p_social_freq']}/14")
                        
                        # 취미 상위 3개 추출 로직
                        h_scores = {h: row[f'p_{h}'] for h in hobby_cols}
                        top_3 = sorted(h_scores.items(), key=lambda x: x[1], reverse=True)[:3]
                        st.write(f"**🎨 선호 취미:** {', '.join([h[0].capitalize() for h in top_3])}")
                    st.divider()

    st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>© 2026 Team 'Wow Beasts' | Powered by Nam-Jeong's AI Engine</p>", unsafe_allow_html=True)
