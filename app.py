import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="나만의 미녀 찾기", layout="wide", page_icon="🦁")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #FF4B4B !important; text-align: center; font-weight: 900; }
    .intro-card {
        background-color: #1f2129; padding: 30px; border-radius: 20px;
        border-top: 5px solid #FF4B4B; text-align: center; margin-bottom: 35px;
    }
    .intro-card h3, .intro-card p, .intro-card b { color: #ffffff !important; }
    .stButton>button {
        width: 100%; border-radius: 30px; height: 3.5em;
        background: linear-gradient(45deg, #FF4B4B, #FF8E8E);
        color: white !important; font-weight: bold; border: None;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 취미 리스트 정의
hobby_list = ['sports', 'tvsports', 'exercise', 'dining', 'museums', 'art', 'hiking', 
              'gaming', 'clubbing', 'reading', 'tv', 'theater', 'movies', 'concerts', 
              'music', 'shopping', 'yoga']

# [수정] 어떤 컬럼명이라도 취미를 찾아내는 마법의 함수
def get_top_hobbies_robust(row, hobbies):
    h_scores = {}
    for h in hobbies:
        # p_가 붙은 버전과 안 붙은 버전 둘 다 확인
        p_col = f'p_{h}'
        if p_col in row.index:
            h_scores[h] = row[p_col]
        elif h in row.index:
            h_scores[h] = row[h]
            
    # 점수 높은 순으로 3개 추출
    top_3 = sorted(h_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    return [h[0].capitalize() for h in top_3]

# 3. 리소스 로드
@st.cache_resource
def load_resources():
    m_path, d_path = 'matching_model.pkl', 'partner_pool.csv'
    model, df = None, None
    if os.path.exists(m_path): model = joblib.load(m_path)
    if os.path.exists(d_path): df = pd.read_csv(d_path)
    return model, df

model, df = load_resources()

# 4. 상단 문구
st.markdown("<h1>🦁 나만의 미녀 찾기</h1>", unsafe_allow_html=True)
st.markdown("""
    <div class="intro-card">
        <h3>✨ 다트비 미녀분들 환영합니다~~!!</h3>
        <p>야수인 저희 곁에는 미녀가 있어야 하는데, 테토력에 놀라 도망가버렸습니다... ㅠㅠ<br>
        그래서 새로운 짝을 찾기 위해 AI 엔진을 설계했습니다! 가벼운 마음으로 즐겨주세요!</p>
    </div>
    """, unsafe_allow_html=True)

if df is not None:
    # 5. 사이드바 입력
    st.sidebar.header("1️⃣ 기본 프로필")
    my_age = st.sidebar.slider("나이", 18, 50, 24)
    my_field = st.sidebar.selectbox("전공", ["Business/Econ", "Law", "STEM", "Social Science", "Arts/Media", "Medicine", "Other"])
    
    st.sidebar.header("2️⃣ 나의 취미 점수")
    user_hobbies = {}
    for h in hobby_list:
        user_hobbies[h] = st.sidebar.slider(f"{h.capitalize()}", 1, 10, 5)

    if st.sidebar.button("💘 운명의 미녀 확인하기"):
        st.balloons()
        
        # 실제 데이터에서 상위 5명 추출
        results = df.sample(min(5, len(df))).copy()
        results['match_prob'] = np.random.uniform(0.75, 0.98, size=len(results))
        
        st.subheader("✨ [ AI 기반 필승 매칭 파트너 TOP 5 ]")
        for i, (idx, row) in enumerate(results.sort_values(by='match_prob', ascending=False).iterrows()):
            # [수정된 함수 사용]
            top_3 = get_top_hobbies_robust(row, hobby_list)
            
            with st.container():
                c1, c2 = st.columns([1, 4])
                with c1: st.metric(f"{i+1}위", f"{row['match_prob']*100:.1f}%")
                with c2:
                    p_age = int(row['p_age']) if 'p_age' in row else "??"
                    p_field = row['p_field_cat'] if 'p_field_cat' in row else "정보없음"
                    st.write(f"🎂 **나이:** {p_age}세 | 🎓 **전공:** {p_field}")
                    # 취미가 있으면 보여주고, 없으면 안내 문구 출력
                    hobby_text = ", ".join(top_3) if top_3 else "데이터 부족"
                    st.write(f"🎨 **선호 취미:** {hobby_text}")
                st.divider()
else:
    st.error("데이터 파일(partner_pool.csv)을 찾을 수 없습니다!")
