import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        cursor_factory=psycopg2.extras.DictCursor
    )
