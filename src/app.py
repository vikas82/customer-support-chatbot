import os
import streamlit as st
from dotenv import load_dotenv

from config import LLM_PROVIDER, GROQ_API_KEY, GROQ_MODEL, OPENAI_API_KEY, OPENAI_MODEL
from agents.team import build_team, run_support

load_dotenv()

def get_model():
    if LLM_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY missing but LLM_PROVIDER=openai")
        from agno.models.openai import OpenAIChat
        return OpenAIChat(id=OPENAI_MODEL, api_key=OPENAI_API_KEY)

    # default: groq
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY missing but LLM_PROVIDER=groq")
    from agno.models.groq import Groq
    return Groq(id=GROQ_MODEL, api_key=GROQ_API_KEY)

st.set_page_config(page_title="Support Bot (RAG + Agno)", page_icon="🤖", layout="wide")

st.title("🤖 :blue[Customer Support chatBot]")
st.subheader(":red[RAG(Chroma) + Agno Agent/Team]")
st.caption(":yellow[A small support desk in one screen: triage → retrieve → tools → answer → escalate (if needed).]", )

with st.sidebar:
    st.subheader("Controls")
    if st.button("🧹 Clear chat"):
        st.session_state.messages = []
        st.rerun()

    # st.markdown("---")
    # st.subheader("Quick Tips")
    # st.write("- Try: “Track my order A1001”")
    # st.write("- Try: “Refund status R2001”")
    # st.write("- Try: “What’s the return policy?”")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about orders, refunds, returns, shipping, products...")
with st.spinner("Generating answer..."):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            model = get_model()
            #st.write("Default Mode - ", model)
            team = build_team(model)

            history_for_logic = st.session_state.messages[:-1]  # everything before current user msg
            reply = run_support(team, user_input, history_for_logic)

        except Exception as e:
            reply = f"Something went wrong on my side: `{e}`\n\nIf you want, paste the error details and I’ll fix it."

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
