import streamlit as st
from src.ai.agent import ProfileExtractorAgent

st.set_page_config(
    page_title = "금융 정책 통합 계산기",
    page_icon = "🏦",
    layout = "wide"
)

# 메인 타이틀
st.title("맞춤형 금융 정책 통합 계산기")
st.markdown("편하게 상황을 이야기하면 AI가 알아서 분석해 드립니다.")

st.divider()

st.subheader("1. 내 프로필 입력")
user_input = st.text_area(
    "현재 상황을 자유롭게 작성해주세요.",
    placeholder = "ex.) 서울에 사는 31세 직장인이야. 연봉은 4500만원이고 무주택 기간은 3년이야.",
    height = 100
)

if st.button("프로필 분석하기"):
    if user_input.strip():
        with st.spinner("AI가 상황 분석 중..."):
            try:
                agent = ProfileExtractorAgent()
                profile_data = agent.extract_profile(user_input)
                if profile_data:
                    st.success("프로필 분석 완료!")
                    st.json(profile_data)
                else:
                    st.error("분석 실패. 문장을 더 자세히 작성해주세요.")
            except Exception as e:
                st.error(f"시스템 오류 발생! - {e}")
    else:
        st.warning("상황을 입력해주세요!")