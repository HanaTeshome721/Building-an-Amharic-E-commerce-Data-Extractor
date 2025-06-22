import sys
import os
import asyncio

# Add root path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Add src path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from src.scraping.telegram_scraper import scrape_channel
from src.confi.telegram_channels import CHANNELS

async def scrape_all_channels():
    for channel in CHANNELS:
        print(f"📦 Scraping from: {channel}")
        await scrape_channel(channel, limit=100)

if __name__ == "__main__":
    asyncio.run(scrape_all_channels())
