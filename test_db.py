import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv(override=True)

# CI lo .env undadu kabatti automatic ga SQLite fallback avuthundi.
# Repu GitHub Secrets lo DATABASE_URL pettiste ade code Neon ki connect avuthundi.
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./rklab.db"

print("⏳ Connecting to:", DATABASE_URL.split("://")[0], "database...")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1;"))
        print("✅ SUCCESS! Database connected!")
        print("📊 Test query returned:", result.scalar())
except Exception as e:
    print("❌ ERROR:", e)