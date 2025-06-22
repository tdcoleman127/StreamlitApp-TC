import streamlit as st
import random

def dummy_code():
    # --- Basic Title and Introduction ---
    st.set_page_config(page_title="SmartPlanner (Beta)", page_icon="🧠")
    st.title("🧠 SmartPlanner — Beta Test")
    st.markdown("""
    Welcome! This is a very early version of a simple planner tool.

    We're gathering feedback to learn what works, what doesn’t, and what confuses you.  
    Just try it out — then leave us a bit of feedback at the end!
    """)

    # --- Inputs for Demo Experience ---
    name = st.text_input("👤 Your name")
    goal = st.text_input("🎯 What's one thing you want to get done today?")

    # --- Generate Fake Plan ---
    if st.button("🚀 Generate Plan"):
        plans = [
            f"{name}, start your day with 10 minutes of deep breathing. Then, work on **'{goal}'** for 90 minutes using the Pomodoro technique.",
            f"{name}, break **'{goal}'** into three steps. Focus for 25 minutes at a time and take 5-minute breaks.",
            f"{name}, schedule **'{goal}'** right after a walk or light stretch. Prime your mind for success!",
            f"{name}, write down why **'{goal}'** matters to you. Then spend 45 focused minutes on it.",
        ]
        st.success(random.choice(plans))

    # --- Feedback Link ---
    st.markdown("---")
    st.subheader("📝 What do you think?")
    st.markdown("We'd really love your thoughts — even if this felt confusing or odd. It helps us improve.")

    # 👇 Replace this URL with your actual deployed feedback form
    st.markdown("[👉 Leave Feedback Here](https://your-feedback-form.streamlit.app)", unsafe_allow_html=True)
