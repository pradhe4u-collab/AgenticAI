"""Streamlit chat UI for Bring Books to Life.

Run:  streamlit run app.py
Needs GROQ_API_KEY in the environment / .env or provided via the sidebar.
"""
import os
import streamlit as st

from agent import BookChat
from personas import PERSONAS, DEFAULT

st.set_page_config(page_title="Bring Books to Life", page_icon="🎭", layout="centered")
st.title("🎭 Bring Books to Life")
st.caption("Chat with a character from a book. They stay in character, answer from the text, and remember you.")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input(
        "Groq API Key",
        value="",
        type="password",
        help="Enter your Groq key here or set GROQ_API_KEY in your .env file.",
    )
    st.caption("Get an API key from [Groq Console](https://console.groq.com/keys).")
    st.markdown("---")

    key = st.selectbox(
        "Character",
        list(PERSONAS),
        format_func=lambda k: PERSONAS[k].name,
        index=list(PERSONAS).index(DEFAULT),
    )
    uploaded = st.file_uploader(
        "Ground this character in your own source (.txt) — keeps their persona",
        type=["txt"],
    )

    if st.button("Start / reset conversation", type="primary"):
        effective_key = api_key_input.strip() or os.getenv("GROQ_API_KEY")
        if not effective_key:
            st.error("⚠️ Please provide a Groq API key to start.")
        else:
            os.environ["GROQ_API_KEY"] = effective_key
            src = uploaded.read().decode("utf-8", "ignore") if uploaded else None
            st.session_state.chat = BookChat(key, source_text=src)
            st.session_state.history = []

# Resolve effective key
effective_key = api_key_input.strip() or os.getenv("GROQ_API_KEY")
if effective_key:
    os.environ["GROQ_API_KEY"] = effective_key

# Initialize session state
if "chat" not in st.session_state:
    if effective_key:
        st.session_state.chat = BookChat(DEFAULT)
    else:
        st.session_state.chat = None
    st.session_state.history = []

# Render chat history
for role, text in st.session_state.history:
    st.chat_message(role).write(text)

# Input handling
char_name = st.session_state.chat.persona.name if st.session_state.chat else PERSONAS[DEFAULT].name
if prompt := st.chat_input(f"Say something to {char_name}…"):
    if not effective_key:
        st.error("⚠️ Groq API key not found. Please enter it in the sidebar or set `GROQ_API_KEY` in your `.env`.")
    else:
        os.environ["GROQ_API_KEY"] = effective_key
        if st.session_state.chat is None:
            st.session_state.chat = BookChat(key)

        st.session_state.history.append(("user", prompt))
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("thinking in character…"):
                reply = st.session_state.chat.say(prompt)
            st.write(reply)
        st.session_state.history.append(("assistant", reply))