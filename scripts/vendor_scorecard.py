
import os
import json
import pandas as pd
from datetime import datetime
from glob import glob

# Directory where raw post JSON files are stored
RAW_DATA_PATH = "data/raw/"
VENDORS = ["Shewabrand", "helloomarketethiopia", "modernshoppingcenter", "qnashcom", "Fashiontera"]

def parse_message(json_path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    timestamp = datetime.fromisoformat(data["timestamp"])
    views = data.get("views", 0)
    text = data.get("text", "")
    price = None

    # Extract price using simple pattern (for better results use your NER model instead)
    for token in text.split():
        if token.isdigit():
            birr_index = text.find("ብር")
            if birr_index != -1:
                try:
                    price = int(token)
                except:
                    pass
                break
    return {"timestamp": timestamp, "views": views, "text": text, "price": price}

def score_vendor(vendor_name):
    message_files = glob(f"{RAW_DATA_PATH}/{vendor_name}/msg_*.json")
    if not message_files:
        return None

    parsed_data = [parse_message(path) for path in message_files]
    df = pd.DataFrame(parsed_data)

    if df.empty:
        return None

    df["week"] = df["timestamp"].dt.isocalendar().week

    # Metrics
    avg_views = df["views"].mean()
    post_frequency = df.groupby("week").size().mean()
    avg_price = df["price"].dropna().astype(float).mean()
    top_post = df.sort_values("views", ascending=False).iloc[0]

    # Simple Lending Score (customize as needed)
    lending_score = (avg_views * 0.5) + (post_frequency * 0.5)

    return {
        "Vendor": vendor_name,
        "Avg. Views/Post": round(avg_views, 2),
        "Posts/Week": round(post_frequency, 2),
        "Avg. Price (ETB)": round(avg_price, 2) if not pd.isna(avg_price) else "N/A",
        "Top Post Text": top_post["text"][:100],
        "Top Post Views": top_post["views"],
        "Lending Score": round(lending_score, 2),
    }

results = [score_vendor(v) for v in VENDORS]
results = [r for r in results if r]

df_scorecard = pd.DataFrame(results)
df_scorecard.to_csv("outputs/vendor_scorecard.csv", index=False)
print("✅ Vendor scorecard saved to outputs/vendor_scorecard.csv")
