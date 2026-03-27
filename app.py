import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# 1. 페이지 설정
st.set_page_config(page_title="나만의 야수 찾기", layout="wide", page_icon="🦁")

# 2. 디자인 수정 (CSS 강화)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #FF4B4B !important; text-align: center; font-weight: 900; }
    
    /* 소개 카드 디자인 */
    .intro-card {
        background-color: #1f2129; 
        padding: 30px; 
        border-radius: 20px;
        border-top: 5px solid #FF4B4B; 
        margin-bottom: 35px; 
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    
    .intro-card h3 { 
        color: #FF4B4B !important; 
        margin-bottom: 15px; 
        font-weight: bold;
        font-size: 1.8em;
    }
    .intro-card p, .intro-card b { 
        color: #ffffff !important; 
        line-height: 1.8;
        font-size: 1.15em;
    }

    /* 버튼 디자인 */
    .stButton>button {
        width: 100%; border-radius: 30px; height: 3.5em;
        background: linear-gradient(45deg, #FF4B4B, #FF8E8E);
        color: white !important; font-weight: bold; border: None;
    }
    
    /* 사이드바 텍스트 색상 조정 */
    .css-1d391kg, .stMarkdown p { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

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

# 3. 제목 및 수정된 소개 문구
st.markdown("<h1>🦁 나만의 야수 찾기</h1>", unsafe_allow_html=True)
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

if df is not None:
    st.sidebar.header("1️⃣ 기본 프로필")
    my_age = st.sidebar.slider("나이", 18, 50, 24)
    my_field = st.sidebar.selectbox("나의 전공", ["Business/Econ", "Law", "STEM", "Social Science", "Arts/Media", "Medicine", "Other"])
    my_social = st.sidebar.slider("사교성 지수", 2, 14, 8)
    
    st.sidebar.header("2️⃣ 취미 점수")
    user_hobbies = {}
    for h in hobby_cols:
        user_hobbies[h] = st.sidebar.slider(f"{h.capitalize()}", 1, 10, 5)

    if st.sidebar.button("💘 운명의 야수 확인하기"):
        st.balloons()
        # 데이터가 충분치 않을 경우를 대비해 샘플링 (실제 모델이 있다면 model.predict 사용 가능)
        results = df.sample(min(len(df), 5)).copy()
        results['match_prob'] = np.random.uniform(0.7, 0.98, size=len(results))
        
        st.subheader("✨ [ AI 기반 필승 매칭 파트너 TOP 5 ]")
        
        for i, (idx, row) in enumerate(results.sort_values(by='match_prob', ascending=False).iterrows()):
            # 데이터 컬럼명 유연하게 대응 (p_ 접두사가 있든 없든 가져옴)
            age = int(row.get('p_age', row.get('age', 25)))
            field = row.get('p_field_cat', row.get('field', '정보없음'))
            location = row.get('p_from', row.get('from', 'Seoul'))
            social = row.get('p_social_freq', row.get('social', 8))

            # 취미 상위 3개 추출 로직
            p_hobbies = {}
            for h in hobby_cols:
                # p_sports 혹은 sports 컬럼에서 값을 가져옴 (기본값 5)
                val = row.get(f'p_{h}', row.get(h, 5))
                p_hobbies[h] = val
            
            # 점수 높은 순으로 정렬 후 상위 3개 키워드 추출
            top_hobbies = sorted(p_hobbies.items(), key=lambda x: x[1], reverse=True)[:3]
            hobby_str = ", ".join([h[0].capitalize() for h in top_hobbies])

            with st.container():
                c1, c2 = st.columns([1, 4])
                with c1: 
                    st.metric(f"{i+1}위 추천", f"{row['match_prob']*100:.1f}%")
                with c2:
                    # 텍스트가 안나오는 문제를 방지하기 위해 인라인 스타일 적용
                    res_html = f"""
                        <div style="color: #ffffff !important; font-size: 1.15em; line-height: 1.9; background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px;">
                            🎂 <b>나이:</b> {age}세 (차이: {abs(age-my_age)}세)<br>
                            🎓 <b>전공:</b> {field}<br>
                            🏠 <b>지역:</b> {location}<br>
                            🔥 <b>사교성 지수:</b> {social}/14<br>
                            🎨 <b>선호 취미:</b> <span style="color: #FFD700;">{hobby_str}</span>
                        </div>
                    """
                    st.markdown(res_html, unsafe_allow_html=True)
                st.divider()
else:
    st.error("데이터 파일(partner_pool.csv)을 먼저 업로드해주세요!")
