import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from telethon.sync import TelegramClient

# =====================
# LOAD ENV
# =====================
load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

# =====================
# SAFETY CHECK (IMPORTANT)
# =====================
if not api_id or not api_hash:
    raise ValueError("Missing API_ID or API_HASH in .env file")

api_id = int(api_id)  # Telethon requires int

# =====================
# LOGGING SETUP
# =====================
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =====================
# TELEGRAM CLIENT
# =====================
client = TelegramClient("session", api_id, api_hash)

# =====================
# CHANNELS
# =====================
CHANNELS = [
    "chemed",
    "lobeliacosmetics",
    "tikvahpharma"
]

# =====================
# SCRAPE FUNCTION
# =====================
async def scrape_channel(channel_name):
    logging.info(f"Starting scrape: {channel_name}")

    messages_data = []

    try:
        entity = await client.get_entity(channel_name)

        async for message in client.iter_messages(entity, limit=50):

            data = {
                "message_id": message.id,
                "channel": channel_name,
                "date": str(message.date),
                "text": message.message or "",   # FIX: avoid None
                "views": message.views or 0,
                "forwards": message.forwards or 0,
                "has_media": bool(message.media)
            }

            # =====================
            # DOWNLOAD IMAGE
            # =====================
            if message.media:
                image_dir = f"data/raw/images/{channel_name}"
                os.makedirs(image_dir, exist_ok=True)

                image_path = f"{image_dir}/{message.id}.jpg"
                await client.download_media(message, file=image_path)

                data["image_path"] = image_path

            messages_data.append(data)

        # =====================
        # SAVE JSON (DATA LAKE)
        # =====================
        today = datetime.now().strftime("%Y-%m-%d")
        json_dir = f"data/raw/telegram_messages/{today}"
        os.makedirs(json_dir, exist_ok=True)

        file_path = f"{json_dir}/{channel_name}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(messages_data, f, indent=4, ensure_ascii=False)

        logging.info(f"Finished scraping: {channel_name}")

    except Exception as e:
        logging.error(f"Error scraping {channel_name}: {str(e)}")


# =====================
# MAIN RUNNER
# =====================
async def main():
    for channel in CHANNELS:
        await scrape_channel(channel)


with client:
    client.loop.run_until_complete(main())