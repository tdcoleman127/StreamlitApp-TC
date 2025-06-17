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
    st.session_state.used_before_input = 1 # Default rating
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
        st.error("❗ Feedback message cannot be empty. Please tell us something!")
        return # Stop if validation fails

    st.success("🎉 Thank you for your feedback! It has been recorded.")
    
    # --- CLEARING THE FORM FIELDS ---
    # Reset the session state variables linked to the input widgets' 'value' parameter
    st.session_state.name_input = ""
    st.session_state.used_before_input = 1 # Reset to default
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

with st.form("My Feedback Form"):
    st.write("Please provide your feedback")

    name = st.text_input(
        "Your Feedback",
        value=st.session_state.name_input, # Linked to input state
        key="name_input_widget", # Unique key for this widget instance
        help="Please describe your experience or suggestion."
    )

    feeling_options = ["Yes 😊", "No 🙁"]

    used_before = st.radio(
        "Have you used Streamlit before?",
        options=feeling_options,
        index=st.session_state.used_before_input, # Linked to input state
        key="used_before_input_widget", # Unique key for this widget instance
        help="Please describe your experience or suggestion."
    )

    rating = st.slider(
    "How would you rate your satisfaction?",
    min_value=1,
    max_value=5,
    value=st.session_state.rating_input, # Linked to session state for control
    key="rating_input_widget", # Unique key for the widget
    help="Rate your experience from 1 (Very Poor) to 5 (Excellent)."
    )
    
    favorites = st.text_area(
        "Your Feedback",
        max_chars=500,
        height=100,
        value=st.session_state.favorites_input, # Linked to input state
        key="favorites_input_widget", # Unique key for this widget instance
        help="Please describe your experience or suggestion."
    )

    comments = st.text_area(
        "Your Feedback",
        max_chars=500,
        height=100,
        value=st.session_state.comments_input, # Linked to input state
        key="comments_input_widget", # Unique key for this widget instance
        help="Please describe your experience or suggestion."
    )

    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
            # Call the handler function with the values captured from the form
            handle_feedback_submission(name, used_before, rating, favorites, comments)

st.markdown("---")
    
if st.session_state.last_submitted_name:
    st.subheader("Your Last Submitted Feedback:")
    st.info("This is what you just submitted:")
    st.write(f"**Feedback:** \"{st.session_state.last_submitted_name}\"")
    st.write(f"**Feedback:** \"{st.session_state.last_submitted_used_before}\"")
    st.write(f"**Rating:** {st.session_state.last_submitted_rating} stars")
    st.write(f"**Feedback:** \"{st.session_state.last_submitted_favorites}\"")
    st.write(f"**Feedback:** \"{st.session_state.last_submitted_comments}\"")
    st.markdown("---")
    st.success("The form above has been reset for new input!")
else:
    st.info("Submit feedback above, and it will appear here!")

st.markdown("---")
st.caption("Form Demo powered by Streamlit")