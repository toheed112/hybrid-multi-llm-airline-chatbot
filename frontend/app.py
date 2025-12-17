import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# Fix path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.graph.workflow import run_graph_v4
from backend.tools.utilities import fetch_user_info

st.title("Swiss Airlines Chatbot")
st.write("Powered by OpenAI Tool Calling + Ollama DeepSeek")

config = {"passenger_id": "000543216"}
if 'history' not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Ask about flights, hotels, or policies:", key="input")
if st.button("Send"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            new_history = run_graph_v4(user_input, config, st.session_state.history)
            st.session_state.history.append({"role": "user", "content": user_input})
            if new_history and new_history[-1]["role"] == "assistant":
                st.session_state.history.append(new_history[-1])
            st.session_state.history = st.session_state.history[-10:]
        st.rerun()

st.subheader("Chat History")
if st.session_state.history:
    for m in st.session_state.history:
        role = "You" if m["role"] == "user" else "Bot"
        st.write(f"**{role}:** {m['content']}")

with st.sidebar:
    st.header("Config")
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

st.caption("Test: 'Search flights from ZUR to London'")