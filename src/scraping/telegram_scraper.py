import os
import json
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
client = TelegramClient("session_name", api_id, api_hash)


async def scrape_channel(channel, limit=100):
    await client.start()

    folder = f"data/raw/{channel}/"
    media_folder = os.path.join(folder, "media")
    os.makedirs(folder, exist_ok=True)
    os.makedirs(media_folder, exist_ok=True)

    # Fetch messages
    history = await client(GetHistoryRequest(
        peer=channel,
        limit=limit,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    download_tasks = []  # For concurrent media download

    for i, message in enumerate(history.messages):
        if not (message.message or message.media):
            continue

        image_path = None
        if message.media:
            image_path = os.path.join(media_folder, f"msg_{message.id}.jpg")

            # Add media download task (will run in parallel)
            download_tasks.append(
                client.download_media(message, file=image_path)
            )

        # Save metadata immediately
        data = {
            "message_id": message.id,
            "text": message.message,
            "timestamp": str(message.date),
            "sender_id": getattr(message.from_id, 'user_id', None),
            "image_path": image_path if message.media else None
        }

        with open(os.path.join(folder, f"msg_{message.id}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        if i % 10 == 0:
            print(f"📦 Processed {i} messages...")

    # Concurrently download media (in bulk)
    if download_tasks:
        print(f"📥 Downloading {len(download_tasks)} media files...")
        await asyncio.gather(*download_tasks, return_exceptions=True)

    print(f"✅ Scraped {len(history.messages)} messages from {channel}")
