import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="❤️"
)

st.title("❤️ 연애상담 챗봇")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("GEMINI_API_KEY를 Secrets에 설정해주세요.")
    st.stop()

# 모델 생성
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
prompt = st.chat_input("연애 고민을 입력하세요")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # 최근 대화 기록 생성
        history_text = ""

        for msg in st.session_state.messages[-10:]:
            role = "사용자" if msg["role"] == "user" else "상담사"
            history_text += f"{role}: {msg['content']}\n"

        full_prompt = f"""
당신은 따뜻하고 공감 능력이 뛰어난 연애상담 전문가입니다.

규칙:
- 공감적으로 답변한다.
- 비난하지 않는다.
- 현실적인 조언을 제공한다.
- 답변은 300자 이내로 작성한다.

대화 내용:
{history_text}

상담 답변:
"""

        response = model.generate_content(full_prompt)
        answer = response.text

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except Exception as e:
        st.error(f"오류 발생: {e}")
