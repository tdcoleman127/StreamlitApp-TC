import requests
import random
import time
import json
import os

# Load secrets or set manually
SUPABASE_URL = os.getenv("SUPABASE_URL") or "https://iueiwlwfhigbeowflzzd.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml1ZWl3bHdmaGlnYmVvd2ZsenpkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA1NDAyMzksImV4cCI6MjA2NjExNjIzOX0.U_xXXIovEQRrHlHMep2_KlfGqQFoxkTpXJfjmcM4WHw"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

FEEDBACK_ENDPOINT = f"{SUPABASE_URL}/rest/v1/feedback"

names = [
    "Liam", "Olivia", "Noah", "Emma", "Ava",
    "James", "Sophia", "Isabella", "Lucas", "Mia",
    "Elijah", "Charlotte", "Amelia", "Benjamin", "Harper",
    "Henry", "Evelyn", "Jack", "Abigail", "Ella"
]

ratings = [1, 2, 3, 4, 5]

favorites_pool = [
    "I loved how smooth the navigation was.",
    "The visuals were really calming.",
    "Quick responses and intuitive layout.",
    "No bugs, and I really liked the onboarding.",
    "Worked better than I expected.",
    "Good experience overall.",
    "It was okay, but nothing stood out.",
    "I’m not sure what I liked.",
    "Not much felt impressive honestly.",
    "The home page was decent, not much else.",
]

comments_pool = [
    "The buttons are a bit confusing.",
    "I wish there were more customization options.",
    "Took me a while to find the submit feature.",
    "Loading felt slow at times.",
    "It could use a dark mode option.",
    "Great design, no issues really.",
    "Felt smooth and professional.",
    "Boring, nothing unique.",
    "App kept freezing on me.",
    "I didn’t enjoy it much at all.",
]

def generate_feedback_entry(name):
    return {
        "name": name,
        "used_before": random.choice(["Yes", "No"]),
        "rating": random.choice(ratings),
        "favorites": random.choice(favorites_pool),
        "comments": random.choice(comments_pool)
    }

def submit_feedback(entry):
    response = requests.post(FEEDBACK_ENDPOINT, headers=HEADERS, json=entry)
    return response.status_code, response.text

if __name__ == "__main__":
    for name in names:
        entry = generate_feedback_entry(name)
        status, text = submit_feedback(entry)
        print(f"{name}: {status} - {text}")
        time.sleep(0.3)  # light delay to avoid rate limiting
