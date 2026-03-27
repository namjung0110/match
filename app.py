import streamlit as st
import pandas as pd
import joblib
import numpy as np

# 1. 페이지 설정 및 디자인 CSS 주입
st.set_page_config(page_title="와 야수들: 운명의 짝 찾기", layout="wide", page_icon="🦁")

# CSS를 사용하여 배경과 글자 스타일 조정
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: None;
    }
    .stSlider [data-baseweb="slider"] {
        margin-bottom: 20px;
    }
    h1 {
        color: #FF4B4B;
        text-align: center;
    }
    .intro-text {
        background-color: #262730;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 25px;
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

# 3. 팀 컨셉 상단 바
st.markdown("<h1>🦁 와 야수들 : 미녀 구출 매칭 시스템</h1>", unsafe_allow_html=True)
st.markdown("""
    <div class="intro-text">
        <h3>✨ 다트비 미녀분들 환영합니다~~!!</h3>
        <p>저희의 엄청난 <b>'테토력'</b>에 놀라 도망간 미녀분들을 다시 찾고 있습니다... ㅠㅠ<br>
        야수들의 진심을 담아 설계한 AI 엔진이 여러분에게 꼭 맞는 짝을 찾아드릴게요!<br>
        가벼운 마음으로 질문에 답하다 보면, 당신의 운명을 발견할지도 모릅니다.</p>
    </div>
    """, unsafe_allow_html=True)

if model is None or df is None:
    st.error("⚠️ 데이터 파일을 불러오지 못했습니다. GitHub 저장소를 확인해주세요.")
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
            my_social = st.slider("사교성 지수 (Social)", 2, 14, 8)
        with col3:
            my_attr = st.slider("자기 객관화 (Self-Attr)", 1, 10, 7)
            my_prob = st.slider("성공 예상치 (Expectation)", 1, 10, 5)

    st.divider()
    
    st.subheader("🎨 17개 취미 월드컵 (당신의 취향은?)")
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
    if st.button("💘 야수들의 선택 확인하기"):
        with st.spinner('야수의 심장으로 운명을 분석 중...'):
            st.balloons()
            
            # (남정님의 추천 로직)
            partner_pool = df.sample(5) # 예시 출력
            
            st.markdown("---")
            st.markdown("## 🏆 AI가 선정한 당신의 '필승 매칭' 파트너")
            
            for i, (idx, row) in enumerate(partner_pool.iterrows()):
                # 디자인된 결과 카드
                with st.container():
                    res_col1, res_col2 = st.columns([1, 3])
                    with res_col1:
                        st.markdown(f"### {i+1}위")
                        st.metric("매칭 확률", f"{np.random.uniform(70, 98):.1f}%")
                    with res_col2:
                        st.markdown(f"**🎂 나이:** {int(row['p_age'])}세  |  **🎓 전공:** {row['p_field_cat']}  |  **🏠 지역:** {row['p_from']}")
                        st.write(f"**🔥 사교성:** {row['p_social_freq']}/14")
                        # 취미 추출 로직 적용
                        h_scores = {h: row[f'p_{h}'] for h in hobby_cols}
                        top_3 = sorted(h_scores.items(), key=lambda x: x[1], reverse=True)[:3]
                        st.write(f"**🎨 선호 취미:** {', '.join([h[0].capitalize() for h in top_3])}")
                    st.divider()

    st.markdown("<p style='text-align:center; color:grey;'>© 2026 Team 'Wow Beasts' | Dartbi Match Project</p>", unsafe_allow_html=True)
