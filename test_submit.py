from datetime import datetime, timedelta
import sqlite3

def submit_test_feedback(name, used_before, rating, favorites, comments, timestamp):
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute(
        '''INSERT INTO feedback (name, used_before, rating, favorites, comments, timestamp)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (name, used_before, rating, favorites, comments, timestamp)
    )
    conn.commit()
    conn.close()
    print(f"✅ Submitted feedback from {name} at {timestamp}")

# Simulate 20 feedback entries with staggered timestamps and stronger sentiment
base_time = datetime.now()
sample_feedback = [
    ("Lena", "Yes", 5, "Super intuitive layout", "I absolutely love this interface — smooth and fast."),
    ("Milo", "No", 1, "Colors?", "Terrible UX. I had no idea what I was clicking."),
    ("Aria", "Yes", 4, "Minimalist color scheme", "Sleek and clean. I appreciated the aesthetic."),
    ("Zane", "No", 2, "The menu", "So confusing. Buttons didn’t make sense."),
    ("Nova", "Yes", 5, "All of it", "Beautifully designed. I enjoyed every second."),
    ("Ivy", "No", 3, "The homepage", "It’s okay. Nothing stood out too much."),
    ("Theo", "Yes", 1, "The fact that it loaded", "Honestly... this was rough to use."),
    ("June", "No", 4, "Animations", "Loved the flow between pages. Super satisfying."),
    ("Ezra", "Yes", 2, "Nothing specific", "Didn't enjoy it. Seemed clunky."),
    ("Niko", "No", 5, "Dark mode and fonts", "Everything was just *right*. Seriously pro work."),
    ("Elle", "Yes", 3, "Font spacing", "Decent. Could be a little more engaging."),
    ("Sage", "No", 1, "I guess the logo?", "Everything else was slow and broken."),
    ("Wren", "Yes", 4, "Simplicity", "Very easy to use. Would recommend."),
    ("Beau", "No", 2, "Side nav bar", "Still not sure where I was supposed to go."),
    ("Liv", "Yes", 5, "User flow", "WOW. Best UX I’ve seen in a while."),
    ("Remy", "No", 3, "Responsiveness", "Fine on desktop. Mobile was kind of laggy."),
    ("Lux", "Yes", 4, "Subtle animations", "Tastefully done. Impressed."),
    ("Orion", "No", 2, "Search bar", "Didn’t work half the time."),
    ("Nia", "Yes", 5, "Layout, icons, colors", "Everything was flawless."),
    ("Kai", "No", 1, "Spacing maybe?", "Didn’t like anything, honestly.")
]

# Submit all with staggered timestamps (1 entry per day back)
for i, entry in enumerate(sample_feedback):
    fake_time = (base_time - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
    submit_test_feedback(*entry, fake_time)
