import os
import streamlit as st
from openai import OpenAI

MODEL = "openai/gpt-oss-120b"
SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer questions clearly and concisely. "
    "If you are not sure about something, say so."
)

st.set_page_config(page_title="Groq Chatbot", page_icon="💬")
st.title("💬 Q&A Chatbot")

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY is not set. Set it in this terminal and run the app again.")
    st.stop()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
)

# Streamlit reruns this script on every interaction, so history lives in session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.write(f"Model: `{MODEL}`")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# Show the existing conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle a new question
if question := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model=MODEL,
                    max_tokens=1000,
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}]
                    + st.session_state.messages,
                )
                answer = response.choices[0].message.content
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        # Remove the unanswered question so history stays valid
        st.session_state.messages.pop()
        st.error(f"Error from API: {e}")