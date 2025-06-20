import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from database import init_db, insert_feedback, clear_feedback
analyzer = SentimentIntensityAnalyzer()


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
    if name.strip() and favorites.strip():
        insert_feedback(name, used_before, rating, favorites, comments)
        st.success("✅ Thanks! Your feedback has been saved.")
    else:
        st.warning("Please fill in your name and some feedback.")

def load_data():
    conn = sqlite3.connect("feedback.db")
    df = pd.read_sql_query("SELECT * FROM feedback ORDER BY timestamp DESC", conn)
    conn.close()
    return df

# Keyword extraction using TextBlob noun phrases
def extract_keywords(text):
    if text:
        blob = TextBlob(text)
        return ", ".join(blob.noun_phrases)
    return ""

# Sentiment analysis using TextBlob polarity
def analyze_sentiment(text):
    if text:
        blob = TextBlob(text)
        return round(blob.sentiment.polarity, 3)  # Range: -1.0 (negative) to 1.0 (positive)
    return 0.0

# Categorized sentiment analysis using TextBlob polarity

def categorize_sentiment(score):
    if score > 0.3:
        return "Positive"
    elif score < -0.3:
        return "Negative"
    else:
        return "Neutral"
    
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def vader_score(text):
    if text:
        return round(analyzer.polarity_scores(text)['compound'], 3)
    return 0.0

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
    st.write("### Collected Feedback for Questions")
    st.dataframe(load_data())  # Display the feedback entries in a table
    
    # Keyword searching and sentiment analysis section
    df = load_data()

    # Apply keyword and sentiment analysis to comments
    df["keywords_favorites"] = df["favorites"].apply(extract_keywords)
    df["sentiment_score_favorites"] = df["favorites"].apply(vader_score)
    df["sentiment_label_favorites"] = df["sentiment_score_favorites"].apply(categorize_sentiment)

    df["keywords_comments"] = df["comments"].apply(extract_keywords)
    df["sentiment_score_comments"] = df["comments"].apply(vader_score)
    df["sentiment_label_comments"] = df["sentiment_score_comments"].apply(categorize_sentiment)

    # Choose which columns to export
    export_df = df[[
        "comments", "keywords_comments", "sentiment_score_comments", "sentiment_label_comments",
        "favorites", "keywords_favorites", "sentiment_score_favorites", "sentiment_label_favorites"
    ]]

    # Convert to CSV
    csv = convert_df_to_csv(export_df)

    # Add download button - now with timestamp!
    # st.download_button(
    #     label="📥 Download Feedback (with Comments & Favorites)",
    #     data=csv,
    #     file_name="feedback_analysis_dual_fields.csv",
    #     mime="text/csv"
    # )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    st.download_button(
        label="📥 Download Feedback CSV",
        data=csv,
        file_name=f"feedback_export_{timestamp}.csv",
        mime="text/csv"
    )

    # st.write("### Comment Sentiment & Keywords")
    # st.dataframe(export_df[["comments", "keywords_comments", "sentiment_score_comments", "sentiment_label_comments"]])

    # st.write("### Favorites Sentiment & Keywords")
    # st.dataframe(export_df[["favorites", "keywords_favorites", "sentiment_score_favorites", "sentiment_label_favorites"]])

    # Display table
    st.write("### Feedback with Keywords and Sentiment")
    st.dataframe(df[["name", "favorites", "comments", "keywords_favorites", "sentiment_score_favorites", "keywords_comments", "sentiment_score_comments"]])

else:
    if admin_password != "":
        st.error("Incorrect password.")