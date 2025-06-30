import streamlit as st
import ollama

# Page config
st.set_page_config(page_title="Chat-Friend", layout="centered")

# Custom styling with spacing and colors
st.markdown(
    """
    <style>
    body {
        background-color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }

    .title-header {
        background-color: #1a237e; /* Dark blue */
        padding: 18px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }

    .user-msg, .bot-msg {
        background-color: #ffffff;
        color: #000000;
        padding: 12px 18px;
        border-radius: 14px;
        max-width: 80%;
        font-size: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 18px;
    }

    .user-msg {
        margin-left: auto;
        margin-right: 0;
    }

    .bot-msg {
        margin-right: auto;
        margin-left: 0;
    }

    footer { display: none; }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown("<div class='title-header'>Chat-Friend</div>", unsafe_allow_html=True)

# Session initialization
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat history with spacing
for msg in st.session_state.history:
    role_class = "user-msg" if msg["role"] == "user" else "bot-msg"
    st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# User chat input
user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    # Limit to recent 6 messages (for performance and context)
    messages = st.session_state.history[-6:]

    with st.spinner("Thinking..."):
        response = ollama.chat(model="phi3:instruct", messages=messages)
        reply = response["message"]["content"]

    st.session_state.history.append({"role": "assistant", "content": reply})
    st.rerun()
