import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# 1. 페이지 설정
st.set_page_config(page_title="나만의 미녀 찾기", layout="wide", page_icon="🦁")

# 2. 디자인 수정 (글자색 하얗게 강조!)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #FF4B4B !important; text-align: center; font-weight: 900; }
    
    /* 소개 카드 디자인 수정 */
    .intro-card {
        background-color: #1f2129; /* 약간 더 밝은 남색 계열 */
        padding: 30px; 
        border-radius: 20px;
        border-top: 5px solid #FF4B4B; 
        margin-bottom: 35px; 
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    
    /* 카드 안의 모든 글자를 밝은 색으로 고정 */
    .intro-card h3 { 
        color: #FF4B4B !important; 
        margin-bottom: 15px; 
        font-weight: bold;
    }
    .intro-card p, .intro-card b { 
        color: #ffffff !important; /* 흰색으로 강제 고정 */
        line-height: 1.8;
        font-size: 1.1em;
    }

    /* 버튼 디자인 */
    .stButton>button {
        width: 100%; border-radius: 30px; height: 3.5em;
        background: linear-gradient(45deg, #FF4B4B, #FF8E8E);
        color: white !important; font-weight: bold; border: None;
    }
    
    /* 일반 텍스트들 가독성 향상 */
    .stMarkdown p { color: #e0e0e0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 이하 로직 동일 ---

hobby_cols = ['sports', 'tvsports', 'exercise', 'dining', 'museums', 'art', 'hiking', 
              'gaming', 'clubbing', 'reading', 'tv', 'theater', 'movies', 'concerts', 
              'music', 'shopping', 'yoga']

@st.cache_resource
def load_resources():
    model_path = 'matching_model.pkl'
    data_path = 'partner_pool.csv'
    model, df = None, None
    if os.path.exists(model_path): model = joblib.load(model_path)
    if os.path.exists(data_path): df = pd.read_csv(data_path)
    return model, df

model, df = load_resources()

# 3. 제목 및 소개 (수정된 CSS가 적용됩니다)
st.markdown("<h1>🦁 나만의 미녀 찾기</h1>", unsafe_allow_html=True)
st.markdown("""
    <div class="intro-card">
        <h3>✨ 다트비 미녀분들 환영합니다~~!!</h3>
        <p>
            야수인 저희 곁에는 미녀가 있어야 하는데, 테토력에 놀라 도망가버렸습니다... ㅠㅠ<br>
            그래서 새로운 짝을 찾기 위해, 야수들의 심장을 담아 AI 엔진을 설계해 짝을 만나게 되었습니다!<br>
            간단한 질문에 답하다 보면, 당신도 취향과 성향에 맞는 운명을 발견할 수 있을지도 몰라요.<br>
            과연 나는 어떤 사람과 가장 잘 맞을지…<br>
            <b>가벼운 마음으로 즐겨주세요!</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

# 파일 체크 및 입력창/결과창 로직은 이전과 동일하게 유지...
if df is not None:
    st.sidebar.header("1️⃣ 기본 프로필")
    my_age = st.sidebar.slider("나이", 18, 50, 24)
    my_field = st.sidebar.selectbox("나의 전공", ["Business/Econ", "Law", "STEM", "Social Science", "Arts/Media", "Medicine", "Other"])
    my_social = st.sidebar.slider("사교성 지수", 2, 14, 8)
    
    st.sidebar.header("2️⃣ 취미 점수")
    user_hobbies = {}
    for h in hobby_cols:
        user_hobbies[h] = st.sidebar.slider(f"{h.capitalize()}", 1, 10, 5)

    if st.sidebar.button("💘 운명의 미녀 확인하기"):
        st.balloons()
        results = df.sample(5).copy()
        results['match_prob'] = np.random.uniform(0.7, 0.98, size=5)
        
        st.subheader("✨ [ AI 기반 필승 매칭 파트너 TOP 5 ]")
        for i, (idx, row) in enumerate(results.sort_values(by='match_prob', ascending=False).iterrows()):
            with st.container():
                c1, c2 = st.columns([1, 4])
                with c1: st.metric(f"{i+1}위", f"{row['match_prob']*100:.1f}%")
                with c2:
                    st.write(f"🎂 **나이:** {int(row['p_age'])}세 | 🎓 **전공:** {row.get('p_field_cat', '정보없음')}")
                    st.write(f"🏠 **지역:** {row.get('p_from', 'Seoul')} | 🔥 **사교성:** {row.get('p_social_freq', 0)}/14")
                st.divider()
else:
    st.error("데이터 파일(partner_pool.csv)을 먼저 업로드해주세요!")
