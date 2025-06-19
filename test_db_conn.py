import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get individual database connection parameters from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Basic validation (optional but good practice)
if not all([DB_HOST, DB_PORT, DB_DATABASE, DB_USER, DB_PASSWORD]):
    print("Error: One or more database credentials (DB_HOST, DB_PORT, DB_DATABASE, DB_USER, DB_PASSWORD) not found in environment variables or .env file.")
    exit()

try:
    # Connect using individual parameters
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT 1;") # Simple query to test connection
    result = cur.fetchone()
    print(f"Database connection successful! Query result: {result}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Database connection FAILED! Error: {e}")