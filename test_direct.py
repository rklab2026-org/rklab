import os
import psycopg
from dotenv import load_dotenv

# Load .env secrets
load_dotenv(override=True)

url = os.getenv("DATABASE_URL")

# Make sure we use psycopg3 driver in connection URL
if url and "psycopg2" in url:
    url = url.replace("psycopg2", "psycopg")

print("⏳ Testing Direct Connection with new psycopg3 driver...")

try:
    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print("✅ BINGO! DIRECT CONNECTION SUCCESSFUL!")
            print(f"📊 PostgreSQL Version: {version[0]}")
except Exception as e:
    print("❌ DIRECT CONNECTION FAILED:")
    print(e)