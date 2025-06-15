import streamlit as st
import pandas as pd

# Tent Feedback Form Title
st.write(""" 
         # Tent App
         And so it begins. 
        """)

# # of submissions subheader with balloons

with st.form("My Feedback Form"):


    # Question 1: Leave your name here
    st.subheader("Leave your name here")

    # Question 2: Have you used a Streamlit app before?
    st.subheader("Have your used a Streamlit app before?")
    
    
    
    # Question 3: Rate this app on a scale of 1 to 5
    st.subheader("Rate this app on a scale of 1 to 5 stars")
    sentiment_mapping = ["one", "two", "three", "four", "five"]
    selected = st.feedback("stars")


    text_input = st.text_input("Enter some text 👇")

    if text_input:
        st.write("You entered: ", text_input)

    if selected is not None:
        st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
    
    # Question 4: What were your favorite and least favorite features?
    st.subheader("What were your favorite and least favorite features?")

    # Question 5: Tell us how we can improve
    st.subheader("Tell us how we can improve")

    st.form_submit_button("Submit")