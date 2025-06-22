import os
import pandas as pd
from src.utils.tokenization import simple_amharic_tokenizer  # ensure src is on your PYTHONPATH

# 🔢 Settings
NUM_TO_LABEL = 50
INPUT_FILE = "data/processed/all_channels_cleaned.csv"
OUTPUT_FILE = "data/labeled/ner_amharic_sample.conll"

# 🛠️ Load data
df = pd.read_csv(INPUT_FILE)
df = df.dropna(subset=["cleaned_text"])
messages = df["cleaned_text"].tolist()
subset = messages[:NUM_TO_LABEL]  # Take first 50 messages

# 📦 Storage for labeled sentences
labeled_sentences = []

# 🧠 Auto-tokenize and assign "O" labels (to be manually edited later)
for text in subset:
    tokens = simple_amharic_tokenizer(text)
    labels = ["O"] * len(tokens)  # default labels are "O" (unlabeled)
    sentence = list(zip(tokens, labels))
    labeled_sentences.append(sentence)

# 💾 Save to CoNLL format
def save_to_conll(sentences, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        for sentence in sentences:
            for token, label in sentence:
                f.write(f"{token}\t{label}\n")
            f.write("\n")  # Blank line separates sentences

save_to_conll(labeled_sentences, OUTPUT_FILE)
print(f"✅ Saved {len(labeled_sentences)} unlabeled messages to {OUTPUT_FILE}")
print("👉 Please open the file and manually label entities using B-Product, I-PRICE, B-LOC, etc.")
