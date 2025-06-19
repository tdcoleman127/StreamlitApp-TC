import sqlite3
import streamlit as st
from database import init_db, insert_feedback, clear_feedback
import pandas as pd

init_db()  # Create the DB table if it doesn't exist

st.title("📝 Tent Feedback Form")
st.write(""" 
         And so it begins. 
        """)

# 5 Feedback Questions
name = st.text_input("What's your name?")
used_before = st.radio("Have you used this app before?", ["Yes", "No"])
rating = st.slider("How would you rate your experience?", 1, 5, 3)
favorites = st.text_area("What did you like most?")
comments = st.text_area("Any other comments or suggestions?")

if st.button("Submit"):
    if favorites.strip() or comments.strip():
        insert_feedback(name, used_before, rating, favorites, comments)
        st.success("✅ Thanks! Your feedback has been saved.")
    else:
        st.warning("Please fill in at least one of the text areas.")

def load_data():
    conn = sqlite3.connect("feedback.db")
    df = pd.read_sql_query("SELECT * FROM feedback ORDER BY timestamp DESC", conn)
    conn.close()
    return df


# Admin password for access
admin_password = st.sidebar.text_input("Enter admin password", type="password")

# If the correct password is entered, show the admin controls
if admin_password == "letmein":  # Change this to a secure password of your choice
    st.write("### Admin Controls")
    
    # Button to clear all feedback
    if st.button("🗑️ Clear All Feedback"):
        clear_feedback()  # Call the function to delete feedback
        st.warning("All feedback entries have been deleted.")
    
    # Show all feedback data
    st.write("### Collected Feedback")
    st.dataframe(load_data())  # Display the feedback entries in a table
else:
    if admin_password != "":
        st.error("Incorrect password.")