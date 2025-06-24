import streamlit as st
import pandas as pd
# "Clean out the fridge"
# Modular imports
from database.feedback import insert_feedback, get_feedback, clear_feedback
from analysis.sentiment import analyze_textblob, analyze_vader
from analysis.keywords import extract_keywords
# from dummy_ui import dummy_code
from recipe.recipe_search import run_recipe_app

API_KEY = st.secrets["SPOONACULAR_API_KEY"]

# Inject Microsoft Clarity script
st.markdown("""
    <script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "s3sokxeysl");
</script>
""", unsafe_allow_html=True)

# ---------------------------
# SECTION: USER FEEDBACK FORM
# ---------------------------
def feedback_form():
    st.title("📋 RecipeTent Feedback Form")
    st.subheader("Please give us feedback on your experience")
    name = st.text_input("Your Name")
    used_before = st.radio("Have you used Streamlit before? (The platform used to make this app)", ["Yes", "No"])
    rating = st.slider("Please rate this app between 1 (Poor) and 5 (Excellent)", 1, 5)
    favorites = st.text_area("What were your favorite features?")
    comments = st.text_area("Any comments or suggestions?")

    if st.button("Submit Feedback"):
        if all([name, used_before, favorites, comments]):
            status, msg = insert_feedback(name, used_before, rating, favorites, comments)
            if status == 201:
                st.success("✅ Submitted! Thanks for your feedback!")
            else:
                st.error(f"❌ Submission failed: {msg}")
        else:
            st.warning("⚠️ Please complete all fields before submitting.")


# ----------------------------
# SECTION: ADMIN DASHBOARD
# ----------------------------
def admin_view():
    st.title("🔐 Admin Dashboard")

    password = st.text_input("Enter Admin Password", type="password")
    if password != "letmein":  # Replace this securely for production
        st.stop()

    st.success("Access granted!")

    feedback = get_feedback()
    if not feedback:
        st.info("No feedback submitted yet.")
        return

    df = pd.DataFrame(feedback)
    st.subheader("📄 Raw Feedback")
    st.dataframe(df)

    # ----------------------------
    # Analyze Sentiment & Keywords
    # ----------------------------
    df["sentiment_comments_vader"] = df["comments"].apply(analyze_vader)
    df["sentiment_comments_blob"] = df["comments"].apply(analyze_textblob)
    df["sentiment_favorites_vader"] = df["favorites"].apply(analyze_vader)
    df["sentiment_favorites_blob"] = df["favorites"].apply(analyze_textblob)

    df["keywords_comments"] = df["comments"].apply(extract_keywords)
    df["keywords_favorites"] = df["favorites"].apply(extract_keywords)

    st.subheader("📊 Sentiment & Keywords Summary")
    st.dataframe(df[[
        "name",
        "sentiment_comments_vader", "sentiment_comments_blob",
        "sentiment_favorites_vader", "sentiment_favorites_blob",
        "keywords_comments", "keywords_favorites"
    ]])

    # ----------------------------
    # Clear Feedback Option
    # ----------------------------
    if st.button("🗑️ Clear All Feedback"):
        status, msg = clear_feedback()
        if status == 204:
            st.success("✅ Feedback cleared.")
        else:
            st.error(f"❌ Failed to clear: {msg}")


# ------------------------
# SECTION: MAIN ROUTER
# ------------------------
def main():
    st.sidebar.title("🧭 Navigation")
    mode = st.sidebar.selectbox("Choose a view", ["User Feedback", "Admin Dashboard"])
    if mode == "User Feedback":
        run_recipe_app()
        feedback_form()
    else:
        admin_view()
main()