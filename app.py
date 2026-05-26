import streamlit as st
from datetime import date

st.set_page_config(page_title="외모관리 앱", page_icon="✨")

st.title("✨ 외모관리 앱")

st.write("오늘의 외모관리 상태를 기록해보세요!")

# 날짜
today = date.today()
st.subheader(f"📅 날짜: {today}")

# 피부 상태
skin = st.selectbox(
    "피부 상태",
    ["좋음", "보통", "트러블 있음"]
)

# 운동 여부
exercise = st.checkbox("오늘 운동했어요 💪")

# 물 마신 양
water = st.slider("오늘 물 마신 양 (잔)", 0, 15, 5)

# 메모
memo = st.text_area("오늘의 메모")

# 저장 버튼
if st.button("기록 저장"):
    st.success("저장 완료! ✨")

    st.write("### 📋 오늘 기록")
    st.write(f"피부 상태: {skin}")

    if exercise:
        st.write("운동: 했음 💪")
    else:
        st.write("운동: 안 함 😢")

    st.write(f"물 마신 양: {water}잔")
    st.write(f"메모: {memo}")
