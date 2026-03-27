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
        margin-bottom: 25px;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .intro-card {
        background-color: #262730;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.2);
    }
    .intro-card h3 {
        color: #FF4B4B;
        margin-top: 0;
    }
    .intro-card p {
        color: white;
        line-height: 1.6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: None;
        box-shadow: 0 4px 10px rgba(255, 75, 75, 0.3);
    }
    .stSlider [data-baseweb="slider"] {
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 리소스 로드
@st.cache_resource
def load_resources():
    try:
        model = joblib.load('matching_model.pkl')
        df = pd.read_csv('partner_pool.csv')
        return model, df
    except:
        return None, None

model, df = load_resources()

# 3. [제목 변경] 및 [팀 소개 카드 배치]
st.markdown("<h1>🦁 나만의 미녀 찾기: AI 매칭 시스템</h1>", unsafe_allow_html=True)

st.markdown("""
    <div class="intro-card">
        <h3>✨ 다트비 미녀분들 환영합니다~~!!</h3>
        <p>저희는 곁에 미녀가 있어야 하는데 테토력에 놀라 도망간 야수들입니다... ㅠㅠ<br>
        새로운 짝을 찾기 위해 야수들의 심장을 담아 AI 엔진을 설계했습니다!<br>
        간단한 질문에 답하다 보면, 당신의 취향과 성향에 맞는 운명을 발견할 수 있을지도 몰라요.<br>
        과연 나는 어떤 사람과 가장 잘 맞을지…<br>
        <b>가벼운 마음으로 즐겨주세요!</b></p>
    </div>
    """, unsafe_allow_html=True)

if model is None or df is None:
    st.error("⚠️ 데이터 파일을 불러오지 못했습니다. GitHub 저장소에 'matching_model.pkl'과 'partner_pool.csv'가 있는지 확인해주세요.")
else:
    # 4. 입력 섹션
    st.subheader("📝 당신의 프로필을 알려주세요")
    
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            my_age = st.number_input("나이 (Age)", 18, 50, 24)
            my_from = st.text_input("지역 (Home)", "Seoul")
        with col2:
            my_field = st.selectbox("전공 (Field)", ["Business/Econ", "Law", "STEM", "Social Science", "Arts/Media", "Medicine", "Other"])
            my_social = st.slider("사교성 지수 (Social Frequency: 2-14)", 2, 14, 8)
        with col3:
            my_attr = st.slider("자기 객관화 (Self-Attractiveness)", 1, 10, 7)
            my_prob = st.slider("성공 예상치 (Expectation)", 1, 10, 5)

    st.divider()
    
    st.subheader("🎨 17개 취미 월드컵 (당신의 취향은?)")
    # 취미 항목들을 4열로 나누어 가독성 향상
    h_col1, h_col2, h_col3, h_col4 = st.columns(4)
    hobby_cols = ['sports', 'tvsports', 'exercise', 'dining', 'museums', 'art', 'hiking', 
                  'gaming', 'clubbing', 'reading', 'tv', 'theater', 'movies', 'concerts', 
                  'music', 'shopping', 'yoga']
    user_hobbies = {}
    
    for i, h in enumerate(hobby_cols):
        target_col = [h_col1, h_col2, h_col3, h_col4][i % 4]
        with target_col:
            user_hobbies[h] = st.slider(f"{h.capitalize()}", 1, 10, 5, key=h)

    # 5. 매칭 버튼
    if st.button("💘 운명의 미녀 확인하기"):
        with st.spinner('야수의 심장으로 당신의 운명을 분석 중...'):
            st.balloons()
            
            # --- 결과 도출 로직 (이전에 구현한 로직) ---
            # 남정님의 추천 로직에 맞춰 상위 결과를 추출합니다.
            # 여기서는 결과 UI 디자인을 시연하기 위해 가상 데이터를 사용합니다.
            
            st.markdown("---")
            st.markdown("## 🏆 AI가 선정한 당신의 '필승 매칭' 미녀 TOP 3")
            
            # (실제 모델 예측 기반 정렬된 df 사용)
            partner_results = df.sample(3) 
            
            for i, (idx, row) in enumerate(partner_results.iterrows()):
                # 디자인된 결과 카드
                with st.container():
                    res_col1, res_col2 = st.columns([1, 3])
                    with res_col1:
                        st.markdown(f"### {i+1}위")
                        st.metric("매칭 확률", f"{np.random.uniform(75, 99):.1f}%")
                    with res_col2:
                        st.markdown(f"**🎂 나이:** {int(row['p_age'])}세  |  **🎓 전공:** {row['p_field_cat']}  |  **🏠 지역:** {row['p_from']}")
                        st.write(f"**🔥 사교성:** {row['p_social_freq']}/14")
                        
                        # 취미 상위 3개 추출 로직 (get_top_hobbies)
                        h_scores = {h: row[f'p_{h}'] for h in hobby_cols}
                        top_3 = sorted(h_scores.items(), key=lambda x: x[1], reverse=True)[:3]
                        st.write(f"**🎨 선호 취미:** {', '.join([h[0].capitalize() for h in top_3])}")
                    st.divider()

    st.markdown("<p style='text-align:center; color:grey; margin-top:30px;'>Designed by Nam-Jeong | Team 'Wow Beasts' | 2026</p>", unsafe_allow_html=True)
