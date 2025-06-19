import sqlite3

DB_NAME = "feedback.db"

# Database Functions

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,  -- Use PRIMARY KEY without AUTOINCREMENT
            name TEXT,
            used_before TEXT,
            rating INTEGER,
            favorites TEXT,
            comments TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def insert_feedback(name, used_before, rating, favorites, comments):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO feedback (name, used_before, rating, favorites, comments)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, used_before, rating, favorites, comments))
    conn.commit()
    conn.close()

def clear_feedback():
    """Clears all feedback from the database."""
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    
    # Delete all rows from the feedback table
    c.execute("DELETE FROM feedback")
    
    # Reset the table structure to ensure fresh sequence
    c.execute('''
        DELETE FROM sqlite_sequence WHERE name='feedback'
    ''')  # Reset the sequence manually if you want to be sure
    
    conn.commit()
    conn.close()

