import streamlit as st
from google import genai
from google.genai import types

# -------------------------
# 페이지 설정
# -------------------------
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💖",
)

st.title("💖 AI 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# -------------------------
# API KEY 불러오기
# -------------------------
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("❌ Streamlit Secrets에 GEMINI_API_KEY를 설정해주세요.")
    st.stop()

# -------------------------
# Gemini Client 생성
# -------------------------
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"❌ Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# -------------------------
# 시스템 프롬프트
# -------------------------
SYSTEM_PROMPT = """
너는 따뜻하고 공감 능력이 뛰어난 연애상담 AI야.

규칙:
- 사용자의 감정을 먼저 공감할 것
- 상대방을 함부로 비난하지 말 것
- 현실적인 조언 제공
- 부드럽고 자연스럽게 대화할 것
- 너무 단정짓지 말 것
- 답변은 한국어로 작성
"""

# -------------------------
# 채팅 기록 초기화
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# 이전 채팅 출력
# -------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------
# 사용자 입력
# -------------------------
user_input = st.chat_input("연애 고민을 입력해보세요...")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):

        with st.spinner("답변 생성 중..."):

            try:
                # 이전 대화 기록 문자열 만들기
                conversation = ""

                for msg in st.session_state.messages:
                    role = "사용자" if msg["role"] == "user" else "AI"
                    conversation += f"{role}: {msg['content']}\n"

                full_prompt = f"""
{SYSTEM_PROMPT}

아래는 지금까지의 대화 내용이야.

{conversation}

위 대화를 참고해서 자연스럽게 이어서 답변해줘.
"""

                # Gemini 호출
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        max_output_tokens=700,
                    )
                )

                ai_response = response.text

                # 응답 출력
                st.markdown(ai_response)

                # 응답 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response
                })

            except Exception as e:
                error_message = f"""
⚠️ 오류가 발생했습니다.

오류 내용:
{str(e)}

잠시 후 다시 시도해주세요.
"""

                st.error(error_message)
