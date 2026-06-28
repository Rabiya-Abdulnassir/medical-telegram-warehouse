import os
import json
from datetime import datetime
from sqlalchemy import create_engine, text

# =====================
# DB CONNECTION
# =====================
DB_URL = "postgresql://postgres:postgres@localhost:5432/telegram_db"

engine = create_engine(DB_URL)

# =====================
# CREATE RAW TABLE
# =====================
def create_table():
    query = """
    CREATE SCHEMA IF NOT EXISTS raw;

    CREATE TABLE IF NOT EXISTS raw.telegram_messages (
        message_id BIGINT,
        channel TEXT,
        message_date TIMESTAMP,
        message_text TEXT,
        views INT,
        forwards INT,
        has_media BOOLEAN,
        image_path TEXT
    );
    """
    with engine.begin() as conn:
        conn.execute(text(query))

# =====================
# LOAD JSON FILES
# =====================
def load_json():
    today = datetime.now().strftime("%Y-%m-%d")
    folder = f"data/raw/telegram_messages/{today}"

    for file in os.listdir(folder):
        if file.endswith(".json"):
            path = os.path.join(folder, file)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

                for row in data:
                    with engine.begin() as conn:
                        conn.execute(text("""
                            INSERT INTO raw.telegram_messages (
                                message_id,
                                channel,
                                message_date,
                                message_text,
                                views,
                                forwards,
                                has_media,
                                image_path
                            )
                            VALUES (
                                :message_id,
                                :channel,
                                :message_date,
                                :message_text,
                                :views,
                                :forwards,
                                :has_media,
                                :image_path
                            )
                        """), {
                            "message_id": row["message_id"],
                            "channel": row["channel"],
                            "message_date": row["date"],
                            "message_text": row["text"],
                            "views": row["views"],
                            "forwards": row["forwards"],
                            "has_media": row["has_media"],
                            "image_path": row.get("image_path")
                        })

# =====================
# RUN
# =====================
if __name__ == "__main__":
    create_table()
    load_json()
    print("Data loaded successfully")
    