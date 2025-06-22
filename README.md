# Amharic E-commerce Data Extractor — Data Preprocessing

This repository contains scripts and utilities to preprocess raw Telegram channel data for Amharic e-commerce messages. The preprocessing cleans and structures the raw data for further Named Entity Recognition (NER) and analysis.

---

## Project Structure

project-root/
├── data/
│ ├── raw/ # Raw JSON message files organized by channel
│ └── processed/ # Output directory for cleaned data files
├── scripts/
│ └── preprocess_data.py # Main preprocessing script
├── src/
│ └── preprocessing/
│ └── text_cleaner.py # Text cleaning utility functions
├── .env # Environment variables (if needed)
├── requirements.txt # Python dependencies
└── README.md # This file

yaml
Copy
Edit

---

## Setup

1. Create and activate a Python virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Add any necessary environment variables to a .env file in the root directory.

Usage
To preprocess all Telegram channels data:

bash
Copy
Edit
python scripts/preprocess_data.py
This script will:

Load raw JSON message files from data/raw/{channel_name}/

Clean message text using Amharic-specific text cleaning functions

Compile cleaned messages into a single DataFrame

Save the cleaned dataset in both Parquet and CSV formats to data/processed/

Functionality Overview
Text Cleaning
Uses clean_amharic_text function in src.preprocessing.text_cleaner to normalize and clean Amharic text messages.

Data Aggregation
Processes all channel folders under data/raw/ and merges them into one dataset.

Output
Saves cleaned data as all_channels_cleaned.parquet and all_channels_cleaned.csv.

Customization
Modify clean_amharic_text in src/preprocessing/text_cleaner.py to adjust text cleaning logic.

Add more preprocessing steps as needed inside scripts/preprocess_data.py.

Troubleshooting
If you encounter ModuleNotFoundError: No module named 'src', ensure you run the script from the project root and/or set the PYTHONPATH environment variable properly.

Ensure the folder structure matches the expected layout.

Use a virtual environment to avoid dependency conflicts.