import streamlit as st
import pandas as pd
from streamlit_star_rating import st_star_rating

# Tent Feedback Form Title
st.write(""" 
         # Tent App
         And so it begins. 
        """)

# # of submissions subheader with balloons

with st.form("My Feedback Form"):
    st.write("Please provide your feedback")

    # Question 1: Leave your name here
    q1 = st.text_input("Question 1: Please leave your name below")

    # Question 2: Have you used a Streamlit app before?
    q2 = st.radio("Question 2: Have you used a Streamlit app before?", ("Yes", "No"))

    # Question 3: Rate this app on a scale of 1 to 5
    q3 = st_star_rating("Question 3: Rate this app on a scale of 1 to 5 stars:", 
                        maxValue=5, defaultValue=3, key="rating")

    # Question 4: What were your favorite and least favorite features?
    q4 = st.text_area("Question 4: What were your favorite and least favorite features?")

    # Question 5: Tell us how we can improve
    q5 = st.text_area("Question 5: Any additional comments?")

    # if selected is not None:
    #     st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

    submit_button = st.form_submit_button("Submit Feedback")

if submit_button:
        st.write("Thank you for your feedback!")
        st.write("Name:", q1)
        st.write("Used Streamlit before:", q2)
        st.write("Star Rating:", q3)
        st.write("Favorite/Least Favorite Features:", q4)
        st.write("Additonal Comments:", q5)