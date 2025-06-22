import streamlit as st

# --- Session State Initialization for Form Inputs ---
# These variables control the *current* state of the form widgets.
# They are reset to clear the form after submission.
if 'feedback_text_input' not in st.session_state:
    st.session_state.feedback_text_input = ""
if 'rating_input' not in st.session_state:
    st.session_state.rating_input = 3 # Default rating
if 'user_category_input' not in st.session_state:
    st.session_state.user_category_input = "General User" # Default category

# --- Session State Initialization for "Last Submitted" Display ---
# These variables hold the details of the very last successful submission
# and are used only for displaying confirmation to the user.
if 'last_submitted_text' not in st.session_state:
    st.session_state.last_submitted_text = None
if 'last_submitted_rating' not in st.session_state:
    st.session_state.last_submitted_rating = None
if 'last_submitted_category' not in st.session_state:
    st.session_state.last_submitted_category = None

# --- Function to Handle Submission and Clearing ---
def handle_feedback_submission(feedback_text, rating, user_category):
    """
    Simulates processing feedback and handles clearing the form
    and updating the 'last submitted' display.
    """
    if not feedback_text.strip():
        st.error("❗ Feedback message cannot be empty. Please tell us something!")
        return # Stop if validation fails

    st.success("🎉 Thank you for your feedback! It has been recorded.")
    
    # --- CLEARING THE FORM FIELDS ---
    # Reset the session state variables linked to the input widgets' 'value' parameter
    st.session_state.feedback_text_input = ""
    st.session_state.rating_input = 3
    st.session_state.user_category_input = "General User" # Reset to default

    # --- UPDATE SESSION STATE FOR "Last Submitted" Display ---
    # Store the just-submitted values to display them below the form
    st.session_state.last_submitted_text = feedback_text
    st.session_state.last_submitted_rating = rating
    st.session_state.last_submitted_category = user_category
    
    st.rerun() # Force a rerun to update the UI (clear form & show last submitted)

# --- Streamlit UI Setup ---
st.set_page_config(layout="centered", page_title="Simple Feedback Form")
st.title("Tell Us What You Think! 🗣️")
st.markdown("---")

# --- Feedback Submission Form ---
st.subheader("Share Your Thoughts")
with st.form("feedback_submission_form", clear_on_submit=False):
    st.write("Please provide your feedback below:")

    # Text Area
    feedback_message = st.text_area(
        "Your Feedback",
        max_chars=500,
        height=150,
        value=st.session_state.feedback_text_input, # Linked to input state
        key="feedback_text_input_widget", # Unique key for this widget instance
        help="Please describe your experience or suggestion."
    )

    # Slider for Rating
    feedback_rating = st.slider(
        "Overall Rating",
        min_value=1,
        max_value=5,
        value=st.session_state.rating_input, # Linked to input state
        key="rating_input_widget", # Unique key for this widget instance
        help="Rate your satisfaction from 1 (Poor) to 5 (Excellent)."
    )
    
    # Selectbox for User Category (Example of an additional variable)
    user_category = st.selectbox(
        "Your User Category",
        ["General User", "Beta Tester", "Premium User", "Guest"],
        index=["General User", "Beta Tester", "Premium User", "Guest"].index(st.session_state.user_category_input), # Set initial value from session state
        key="user_category_input_widget", # Unique key for this widget instance
        help="Select the category that best describes you."
    )

    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        # Call the handler function with the values captured from the form
        handle_feedback_submission(feedback_message, feedback_rating, user_category)

st.markdown("---")

# --- Display Last Submitted Feedback (User Confirmation) ---
# This section will only show details after a successful submission
if st.session_state.last_submitted_text:
    st.subheader("Your Last Submitted Feedback:")
    st.info("This is what you just submitted:")
    st.write(f"**Feedback:** \"{st.session_state.last_submitted_text}\"")
    st.write(f"**Rating:** {st.session_state.last_submitted_rating} stars")
    st.write(f"**Category:** {st.session_state.last_submitted_category}")
    st.markdown("---")
    st.success("The form above has been reset for new input!")
else:
    st.info("Submit feedback above, and it will appear here!")

st.markdown("---")
st.caption("Form Demo powered by Streamlit")