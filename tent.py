import streamlit as st
import pandas as pd
from streamlit_star_rating import st_star_rating

# Tent Feedback Form Title
st.write(""" 
         # Tent App
         And so it begins. 
        """)

# Initializing the session state

if 'name_input' not in st.session_state:
    st.session_state.name_input = ""
if 'used_before_input' not in st.session_state:
    st.session_state.used_before_input = 0 # Default rating
if 'rating_input' not in st.session_state:
    st.session_state.rating_input = 3 # Default rating
if 'favorites_input' not in st.session_state:
    st.session_state.favorites_input = "" # Default rating
if 'comments_input' not in st.session_state:
    st.session_state.comments_input = "" # Default rating

if 'last_submitted_name' not in st.session_state:
    st.session_state.last_submitted_name = None
if 'last_submitted_used_before' not in st.session_state:
    st.session_state.last_submitted_used_before = None
if 'last_submitted_rating' not in st.session_state:
    st.session_state.last_submitted_rating = None
if 'last_submitted_favorites' not in st.session_state:
    st.session_state.last_submitted_favorites = None
if 'last_submitted_comments' not in st.session_state:
    st.session_state.last_submitted_comments = None


# --- Function to Handle Submission and Clearing ---
def handle_feedback_submission(name, used_before, rating, favorites, comments):
    """
    Simulates processing feedback and handles clearing the form
    and updating the 'last submitted' display.
    """
    if not name.strip():
        st.error("❗ Please enter your name and give us some feedback!")
        return # Stop if validation fails
    if not favorites.strip():
        st.error("❗ Please give feedback on the app features!")
        return # Stop if validation fails

    st.success("🎉 ~Yeah! Thank you for your feedback! It has been recorded.")
    
    # --- CLEARING THE FORM FIELDS ---
    # Reset the session state variables linked to the input widgets' 'value' parameter
    st.session_state.name_input = ""
    st.session_state.used_before_input = 0 # Reset to default
    st.session_state.rating_input = 3
    st.session_state.favorites_input = ""
    st.session_state.comments_input = ""


    # --- UPDATE SESSION STATE FOR "Last Submitted" Display ---
    # Store the just-submitted values to display them below the form
    st.session_state.last_submitted_name = name
    st.session_state.last_submitted_used_before = used_before
    st.session_state.last_submitted_rating = rating
    st.session_state.last_submitted_favorites = favorites
    st.session_state.last_submitted_comments = comments

    
    st.rerun() # Force a rerun to update the UI (clear form & show last submitted)

# # of submissions subheader with balloons

with st.form("Tent Feedback Form"):
    st.write("Please provide any feedback about this app")

    name = st.text_input(
        "Question 1: Please leave your name below",
        value=st.session_state.name_input, # Linked to input state
        key="name_input_widget", # Unique key for this widget instance
        help="Please enter your name below"
    )

    choice_options = ["Yes 😊", "No 🙁"]

    used_before = st.radio(
        "Question 2: Have you used a Streamlit app before?",
        options=choice_options,
        index=st.session_state.used_before_input, # Linked to input state
        key="used_before_input_widget", # Unique key for this widget instance
        help="If you've used Streamlit before, select Yes. if not, select No."
    )

    rating = st.slider(
    "Question 3: Rate this app on a scale of 1 to 5 stars:",
    min_value=1,
    max_value=5,
    value=st.session_state.rating_input, # Linked to session state for control
    key="rating_input_widget", # Unique key for the widget
    help="Rate your experience from 1 (Very Poor) to 5 (Excellent)."
    )
    
    favorites = st.text_area(
        "Question 4: What were your favorite and least favorite features?",
        max_chars=500,
        height=100,
        value=st.session_state.favorites_input, # Linked to input state
        key="favorites_input_widget", # Unique key for this widget instance
        help="What did you like most about this app? What should be improved in the future?"
    )

    comments = st.text_area(
        "Question 5: Any additional comments?",
        max_chars=500,
        height=100,
        value=st.session_state.comments_input, # Linked to input state
        key="comments_input_widget", # Unique key for this widget instance
        help="Please describe your experience with this app or suggestions."
    )

    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
            # Call the handler function with the values captured from the form
            handle_feedback_submission(name, used_before, rating, favorites, comments)

st.markdown("---")
    
if st.session_state.last_submitted_name:
    st.subheader("Your Last Submitted Feedback:")
    st.info("This is what you just submitted:")
    st.write(f"**Name:** \"{st.session_state.last_submitted_name}\"")
    st.write(f"**Used Streamlit Before?:** \"{st.session_state.last_submitted_used_before}\"")
    st.write(f"**Rating:** {st.session_state.last_submitted_rating} stars")
    st.write(f"**Favorite/Least Favorite Features:** \"{st.session_state.last_submitted_favorites}\"")
    st.write(f"**Comments:** \"{st.session_state.last_submitted_comments}\"")
    st.markdown("---")
    st.success("Feel free to enter new feedback for display above!")
else:
    st.info("Submit feedback above, and it will appear here!")

st.markdown("---")
st.caption("Tent App powered by Streamlit")