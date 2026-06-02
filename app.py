import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="축구 챗봇",
    page_icon="⚽",
)

st.title("⚽ 축구 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 초기화 오류: {e}")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! ⚽ 축구 관련 질문을 해주세요. 선수, 전술, 리그, 경기 분석 등 무엇이든 가능합니다."
        }
    ]

# 기존 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
prompt = st.chat_input("축구에 대해 질문해보세요")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # 대화 기록 구성
        history = ""

        for msg in st.session_state.messages:
            role = "사용자" if msg["role"] == "user" else "챗봇"
            history += f"{role}: {msg['content']}\n"

        soccer_prompt = f"""
당신은 축구 전문 AI 코치입니다.

규칙:
- 축구 관련 질문에 전문적으로 답변한다.
- 선수, 전술, 리그, 경기 분석에 강하다.
- 친절하고 이해하기 쉽게 설명한다.

대화 기록:
{history}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=soccer_prompt
        )

        answer = response.text

    except Exception as e:
        answer = f"오류가 발생했습니다.\n\n{str(e)}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

# 사이드바
with st.sidebar:
    st.header("⚽ 축구 챗봇")

    if st.button("대화 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "안녕하세요! ⚽ 축구 관련 질문을 해주세요."
            }
        ]
        st.rerun()
