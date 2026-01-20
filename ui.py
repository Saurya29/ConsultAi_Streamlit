# ui.py

import streamlit as st
import base64

from llm_file import llm
from retriever_setup import (
    prepare_retriever,
    learning_retriever,
    case_prep_retriever
)

from prepare_chain import load_prepare_chain
from learning_chain import load_learning_chain
from case_prep_chain import load_case_prep_chain
from case_example import load_case_examples_chain


# -------------------- UI SETUP --------------------

st.set_page_config(page_title="ConsultBot", layout="wide")
st.title("🤖 ConsultBot – Your Case Interview Coach")


def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/avif;base64,{encoded_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    .block-container {{
        background-color: rgba(0, 0, 0, 0.7);
        padding: 2rem;
        border-radius: 10px;
        color: white;
    }}
    .stTextInput input,
    .stTextArea textarea {{
        background-color: rgba(30, 30, 30, 0.8);
        color: white;
    }}
    .stButton > button {{
        background-color: #1f1f1f;
        color: white;
        border: 1px solid #ccc;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


set_bg("modern-boardroom-ready-meeting_1286777-1867.avif")


# -------------------- LOAD CHAINS --------------------

prepare_chain = load_prepare_chain(llm, prepare_retriever)
learning_chain = load_learning_chain(llm, learning_retriever)
case_prep_chain = load_case_prep_chain(llm)
case_example_chain = load_case_examples_chain(llm, case_prep_retriever)


# -------------------- TABS --------------------

tab1, tab2, tab3, tab4 = st.tabs(
    ["💼 Prepare Yourself", "🎯 Case Prep", "📘 Learning", "🧠 Case Examples"]
)


# -------------------- TAB 1: PREPARE YOURSELF --------------------

with tab1:
    st.subheader("💼 Interview Preparation Help")

    if "chat_prepare" not in st.session_state:
        st.session_state.chat_prepare = []

    user_q = st.text_input("Ask a preparation question:")

    if st.button("Ask") and user_q:
        with st.spinner("Thinking..."):
            response = prepare_chain.invoke(user_q)
            st.session_state.chat_prepare.append(("You", user_q))
            st.session_state.chat_prepare.append(("Coach", response))

    if st.button("Reset Chat"):
        st.session_state.chat_prepare = []

    for role, msg in st.session_state.chat_prepare:
        st.chat_message(role).write(msg)


# -------------------- TAB 2: CASE PREP --------------------

with tab2:
    st.subheader("🎯 Mock Case Interview")

    case_types = {
        "Profitability": "A retail chain has seen a drop in profits.",
        "Market Entry": "A beverage company wants to enter India.",
        "M&A": "A firm is considering acquiring a competitor.",
        "Growth Strategy": "A SaaS company wants 30% growth in 2 years."
    }

    if "case_history" not in st.session_state:
        st.session_state.case_history = []

    case_choice = st.selectbox("Choose a case type:", list(case_types.keys()))

    if st.button("Start Interview"):
        intro = case_prep_chain.invoke(
            f"Start a case interview. Case type: {case_choice}. Prompt: {case_types[case_choice]}"
        )
        st.session_state.case_history = [("🤖", intro)]

    for role, msg in st.session_state.case_history:
        st.markdown(f"**{role}**: {msg}")

    user_input = st.text_input("Your response:")

    if st.button("Send Response") and user_input:
        st.session_state.case_history.append(("🧑", user_input))
        reply = case_prep_chain.invoke(user_input)
        st.session_state.case_history.append(("🤖", reply))

    if st.button("End Interview"):
        feedback = case_prep_chain.invoke(
            "Please evaluate my case interview performance."
        )
        st.markdown("### 🧠 Interviewer Feedback")
        st.write(feedback)
        st.session_state.case_history = []


# -------------------- TAB 3: LEARNING --------------------

with tab3:
    st.subheader("📘 Learn Consulting Concepts")

    if "chat_learning" not in st.session_state:
        st.session_state.chat_learning = []

    user_q = st.text_input("Ask a consulting theory question:")

    if st.button("Ask", key="learn") and user_q:
        with st.spinner("Thinking..."):
            response = learning_chain.invoke(user_q)
            st.session_state.chat_learning.append(("You", user_q))
            st.session_state.chat_learning.append(("Tutor", response))

    if st.button("Reset Chat", key="reset_learn"):
        st.session_state.chat_learning = []

    for role, msg in st.session_state.chat_learning:
        st.chat_message(role).write(msg)


# -------------------- TAB 4: CASE EXAMPLES --------------------

with tab4:
    st.subheader("🧠 Real Case Examples")

    if "chat_examples" not in st.session_state:
        st.session_state.chat_examples = []

    user_q = st.text_input("Ask for a case example:")

    if st.button("Fetch Example") and user_q:
        with st.spinner("Retrieving case..."):
            response = case_example_chain.invoke(user_q)
            st.session_state.chat_examples.append(("You", user_q))
            st.session_state.chat_examples.append(("Trainer", response))

    if st.button("Reset Chat", key="reset_examples"):
        st.session_state.chat_examples = []

    for role, msg in st.session_state.chat_examples:
        st.chat_message(role).write(msg)
