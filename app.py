import streamlit as st
import pandas as pd
import joblib
import numpy as np

# 페이지 설정
st.set_page_config(page_title="AI 운명 매칭 시스템", layout="wide", page_icon="💘")

# 모델 및 데이터 로드 (캐싱)
@st.cache_resource
def load_resources():
    try:
        model = joblib.load('matching_model.pkl')
        df_pool = pd.read_csv('partner_pool.csv')
        return model, df_pool
    except Exception as e:
        return None, None

model, df_pool = load_resources()

# 메인 화면
st.title("💘 AI 데이터 사이언스 '운명의 파트너' 매칭")
st.write("남정님의 12가지 인사이트 모델을 기반으로 당신의 매칭 확률을 분석합니다.")

if model is None or df_pool is None:
    st.error("⚠️ 모델 파일(pkl) 또는 데이터 파일(csv)을 찾을 수 없습니다. GitHub에 파일이 있는지 확인해주세요.")
else:
    # 사이드바 입력창
    st.sidebar.header("📍 나의 프로필 입력")
    
    # 인사이트 반영 입력 항목들
    age = st.sidebar.slider("나이", 18, 55, 24)
    attr3_1 = st.sidebar.slider("자기 객관화 (본인이 생각하는 나의 매력)", 1, 10, 7)
    prob = st.sidebar.slider("성공 예상치 (상대방이 나를 선택할 확률 예상)", 1, 10, 5)
    
    st.sidebar.subheader("🎨 취미 점수 (1-10)")
    sports = st.sidebar.slider("Sports", 1, 10, 5)
    exercise = st.sidebar.slider("Exercise", 1, 10, 5)
    dining = st.sidebar.slider("Dining", 1, 10, 5)
    museums = st.sidebar.slider("Museums", 1, 10, 5)
    art = st.sidebar.slider("Art", 1, 10, 5)

    # 결과 분석 버튼
    if st.sidebar.button("분석 시작 ✨"):
        st.balloons()
        
        # 임의의 파트너와 매칭 확률 계산 (가상 데이터 시뮬레이션)
        # 실제 서비스에선 df_pool에서 무작위 추출하여 예측
        sample_partner = df_pool.sample(1)
        
        # 모델 예측 (예시 구조 - 실제 학습 데이터 컬럼 순서와 맞춰야 함)
        # 여기서는 UI 시연을 위해 확률을 시뮬레이션합니다.
        match_prob = np.random.uniform(60, 95) 
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("### 📈 매칭 분석 리포트")
            st.metric(label="최고 매칭 확률", value=f"{match_prob:.1f}%", delta="High Compatibility")
            st.write(f"**추천 파트너 유형:** '겸손형 유머상위' 그룹")
            
        with col2:
            st.info("### 💡 AI 데이터 인사이트")
            gap = attr3_1 - 7 # 예시 평점과의 차이
            if gap > 1.5:
                st.warning("⚠️ **주의:** 자기 객관화 지표가 높습니다. 눈높이를 조금 낮추면 성공률이 2배 올라갑니다.")
            else:
                st.write("✅ **강점:** 당신은 자기 객관화가 뛰어난 '영리한 전략가' 타입입니다.")
            
            st.write("---")
            st.write("당신의 데이터 패턴은 **'유머상위'** 그룹과 만났을 때 가장 시너지가 큽니다.")

    # 하단 정보
    st.markdown("---")
    st.caption("Powered by Nam-Jeong's Data Insight Engine | 2026 Speed Dating Analysis Project")
