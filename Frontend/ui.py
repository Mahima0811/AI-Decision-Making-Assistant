import streamlit as st
def load_ui():

    st.markdown("""
    <style>

    .stApp {
        background-color: #0f172a;
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: linear-gradient(to right, #00c6ff, #0072ff);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
    ">

    <h1 style="
        color:white;
        font-size:55px;
    ">
    🤖 AI Decision-Making Assistant
    </h1>

    <p style="
        color:white;
        font-size:22px;
    ">
    Smart AI-powered comparison platform
    </p>

    </div>
    """, unsafe_allow_html=True)