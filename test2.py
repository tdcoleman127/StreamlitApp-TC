import os
import nltk
import streamlit as st
import pandas as pd
from textblob import TextBlob
from sqlalchemy.sql import text # Import text for executing raw SQL

# --- Streamlit UI Layout (MUST BE THE FIRST ST. COMMAND after imports) ---
st.set_page_config(layout="wide", page_title="App Feedback System")

# --- NLTK Downloads (corrected and optimized for Streamlit) ---
@st.cache_resource
def download_nltk_data():
    """Downloads necessary NLTK data if not already present."""
    nltk_data_path = os.path.join(os.path.dirname(__file__), '.nltk_data')
    nltk.data.path.append(nltk_data_path)
    os.environ['NLTK_DATA'] = nltk_data_path # Also set env var for good measure

    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)

    try:
        nltk.data.find('corpora/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger', quiet=True)

# Call the function to ensure data is downloaded once at startup
download_nltk_data()

# --- Database Connection ---
st.write("--- Debugging Secrets ---")
try:
    if "DATABASE_URL" in st.secrets:
        st.write(f"DATABASE_URL found in secrets. First 20 chars: {st.secrets['DATABASE_URL'][:20]}...")
    else:
        st.write("DATABASE_URL NOT found in secrets.")
    # Ensure url is passed to st.connection
    conn = st.connection("render_pg", type="sql", url=st.secrets["DATABASE_URL"])
    st.success("Database connection object created successfully and URL provided.")

except Exception as e:
    st.error(f"Failed to establish database connection: {e}")
    st.stop()


# --- Helper Function for AI Analysis (Sentiment, Keywords) ---
def analyze_text(text_input):
    if not text_input:
        return 0.0, "Neutral", []

    blob = TextBlob(text_input)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0.05:
        sentiment_label = "Positive"
    elif sentiment_score < -0.05:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    # Extract keywords (simple approach: nouns and adjectives)
    keywords = [word.lemmatize() for word, tag in blob.pos_tags if tag.startswith('N') or tag.startswith('J')]
    return sentiment_score, sentiment_label, list(set(keywords)) # Return unique keywords


# --- Function to Add Feedback to Database ---
def add_feedback_to_db(name, used_before, rating, favorites, comments,
                       sentiment_score_comments, sentiment_label_comments, keywords_comments,
                       sentiment_score_favorites, sentiment_label_favorites, keywords_favorites):
    if conn is None:
        st.error("Database connection not established. Cannot add feedback.")
        return False

    try:
        # This is the crucial change: Using conn.query() directly for INSERT.
        # Streamlit handles transactions automatically when using query() for DML.
        conn.query(
            """
            INSERT INTO feedback (
                name, used_before, rating, favorites, comments,
                sentiment_score_comments, sentiment_label_comments, keywords_comments,
                sentiment_score_favorites, sentiment_label_favorites, keywords_favorites
            ) VALUES (
                :name_val, :used_before_val, :rating_val, :favorites_val, :comments_val,
                :sentiment_score_comments_val, :sentiment_label_comments_val, :keywords_comments_val,
                :sentiment_score_favorites_val, :sentiment_label_favorites_val, :keywords_favorites_val
            )
            """,
            params={
                "name_val": name,
                "used_before_val": used_before,
                "rating_val": rating,
                "favorites_val": favorites,
                "comments_val": comments,
                "sentiment_score_comments_val": sentiment_score_comments,
                "sentiment_label_comments_val": sentiment_label_comments,
                "keywords_comments_val": keywords_comments,
                "sentiment_score_favorites_val": sentiment_score_favorites,
                "sentiment_label_favorites_val": sentiment_label_favorites, # Passed directly as a parameter
                "keywords_favorites_val": keywords_favorites
            }
        )
        st.success("🎉 Thank you for your feedback! It has been recorded.")
        # Clear form fields after successful submission
        st.session_state.name = ""
        st.session_state.used_before = False
        st.session_state.rating = 3
        st.session_state.favorites = ""
        st.session_state.comments = ""
        st.experimental_rerun() # Rerun the app to refresh the form and dashboard

        return True
    except Exception as e:
        st.error(f"Failed to submit feedback. Error: {e}")
        st.warning("Please try again or contact support if the issue persists.")
        return False

# --- Function to Fetch All Feedback ---
@st.cache_data(ttl=600) # Cache data for 10 minutes
def get_all_feedback():
    try:
        df = conn.query("SELECT * FROM feedback ORDER BY timestamp DESC") # Removed .df()
        # Process keywords columns which might be stored as string representations of lists/arrays
        for col in ['keywords_comments', 'keywords_favorites']:
            if col in df.columns and df[col].dtype == object:
                # This safely converts string representations of lists (e.g., "{'word1', 'word2'}")
                # to actual Python lists. Adjust if your database stores them differently (e.g., JSON string)
                df[col] = df[col].apply(
                    lambda x: [item.strip().replace('"', '') for item in x.strip('{}').split(',')] if pd.notnull(x) and x not in ('{}', '') else []
                )
        return df
    except Exception as e:
        st.error(f"Error fetching feedback: {e}")
        return pd.DataFrame()


# --- Streamlit UI Components ---

st.title("App Feedback System")

st.markdown("""
    Welcome to the App Feedback System!
    Your feedback helps us improve. Please share your thoughts below.
""")

# Initialize session state for form fields if not already present
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'used_before' not in st.session_state:
    st.session_state.used_before = False
if 'rating' not in st.session_state:
    st.session_state.rating = 3
if 'favorites' not in st.session_state:
    st.session_state.favorites = ""
if 'comments' not in st.session_state:
    st.session_state.comments = ""

with st.form("feedback_form", clear_on_submit=False): # Changed to False for manual clearing
    st.subheader("Submit Your Feedback")

    name = st.text_input("Your Name (Optional)", key="name")
    used_before = st.checkbox("Have you used this app before?", key="used_before")
    rating = st.slider("Rate your experience (1-5 stars)", 1, 5, 3, key="rating")
    favorites = st.text_area("What do you like most about the app?", key="favorites")
    comments = st.text_area("Any other comments or suggestions?", key="comments")

    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        # Perform AI analysis
        comments_sentiment_score, comments_sentiment_label, comments_keywords = analyze_text(comments)
        favorites_sentiment_score, favorites_sentiment_label, favorites_keywords = analyze_text(favorites) # Ensure this is defined here

        success = add_feedback_to_db(
            name.strip(),
            used_before,
            rating,
            favorites.strip(),
            comments.strip(),
            comments_sentiment_score,
            comments_sentiment_label,
            comments_keywords,
            favorites_sentiment_score,
            favorites_sentiment_label, # Use the defined variable
            favorites_keywords
        )
        # The add_feedback_to_db function now handles success message and rerun

st.markdown("---")

# --- Feedback Analysis Dashboard ---
st.header("Feedback Analysis Dashboard")

all_feedback_df = get_all_feedback()

if all_feedback_df.empty:
    st.info("No feedback has been submitted yet, or there was an issue fetching data.")
else:
    st.subheader("All User Feedback")

    # Filtering options
    col_filter_1, col_filter_2, col_filter_3 = st.columns(3)
    with col_filter_1:
        sentiment_filter = st.selectbox(
            "Filter by Comments Sentiment:",
            options=["All", "Positive", "Neutral", "Negative"]
        )
    with col_filter_2:
        used_before_filter = st.selectbox(
            "Filter by Used Before:",
            options=["All", "Yes", "No"]
        )
    with col_filter_3:
        comments_keyword_search = st.text_input("Search keywords in comments (e.g., 'fast', 'bug')")

    filtered_df = all_feedback_df.copy()

    if sentiment_filter != "All":
        filtered_df = filtered_df[filtered_df['sentiment_label_comments'] == sentiment_filter]

    if used_before_filter != "All":
        bool_val = True if used_before_filter == "Yes" else False
        filtered_df = filtered_df[filtered_df['used_before'] == bool_val]

    if comments_keyword_search:
        comments_keyword_search = comments_keyword_search.lower()
        # Filter where keywords_comments (list) contains the search term or comments (string) contains it
        filtered_df = filtered_df[
            filtered_df['keywords_comments'].apply(lambda x: any(comments_keyword_search in k.lower() for k in x) if isinstance(x, list) else False) | # Handle non-list types
            filtered_df['comments'].str.contains(comments_keyword_search, case=False, na=False)
        ]

    # Display the filtered DataFrame
    st.dataframe(filtered_df, use_container_width=True)

    # --- Basic Visualizations ---
    st.subheader("Key Trends & Visualizations")
    col_viz_A, col_viz_B, col_viz_C = st.columns(3)
    with col_viz_A:
        st.write("Comments Sentiment Distribution:")
        sentiment_counts = filtered_df['sentiment_label_comments'].value_counts()
        st.bar_chart(sentiment_counts)
    with col_viz_B:
        st.write("Overall Rating Distribution:")
        rating_counts = filtered_df['rating'].value_counts().sort_index()
        st.bar_chart(rating_counts)
    with col_viz_C:
        st.write("'Used Before' Distribution:")
        used_before_counts = filtered_df['used_before'].map({True: 'Yes', False: 'No'}).value_counts()
        st.bar_chart(used_before_counts)

    # --- Download Filtered Data ---
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Feedback as CSV",
        data=csv_data,
        file_name="filtered_feedback.csv",
        mime="text/csv",
    )