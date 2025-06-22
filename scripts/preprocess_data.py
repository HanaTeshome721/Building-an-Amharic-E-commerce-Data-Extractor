import os
import sys
import json
import pandas as pd
from dotenv import load_dotenv

# ✅ Fix: Add root path to sys.path for 'src' to be discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocessing.text_cleaner import clean_amharic_text  # Make sure this exists

load_dotenv()

RAW_BASE = "data/raw"
PROCESSED_BASE = "data/processed"
os.makedirs(PROCESSED_BASE, exist_ok=True)

def load_and_clean_channel(channel_name):
    folder = os.path.join(RAW_BASE, channel_name)
    files = [f for f in os.listdir(folder) if f.endswith(".json")]

    records = []

    for file in files:
        path = os.path.join(folder, file)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        raw_text = data.get("text", "")
        if not raw_text:
            continue

        cleaned = clean_amharic_text(raw_text)

        records.append({
            "channel": channel_name,
            "message_id": data.get("message_id"),
            "cleaned_text": cleaned,
            "timestamp": data.get("timestamp"),
            "sender_id": data.get("sender_id"),
            "image_path": data.get("image_path")
        })

    return pd.DataFrame(records)

def preprocess_all_channels():
    all_dfs = []

    for channel in os.listdir(RAW_BASE):
        channel_path = os.path.join(RAW_BASE, channel)
        if os.path.isdir(channel_path):
            print(f"🧼 Preprocessing channel: {channel}")
            df = load_and_clean_channel(channel)
            all_dfs.append(df)

    full_df = pd.concat(all_dfs, ignore_index=True)
    full_df.to_parquet(os.path.join(PROCESSED_BASE, "all_channels_cleaned.parquet"))
    full_df.to_csv(os.path.join(PROCESSED_BASE, "all_channels_cleaned.csv"), index=False)
    print(f"✅ Saved cleaned data: {len(full_df)} messages")

if __name__ == "__main__":
    preprocess_all_channels()
