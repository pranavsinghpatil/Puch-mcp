import pandas as pd
import os

# Path to your downloaded Kaggle dataset
RAW_DATA_PATH = "raw.csv"  # change if filename is different
OUTPUT_DIR = "."
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "recipes.csv")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load dataset
print("[INFO] Loading dataset...")
df = pd.read_csv(RAW_DATA_PATH)

# Keep only required columns
required_columns = [
    "name", "image_url", "description", "cuisine", "course",
    "diet", "prep_time", "ingredients", "instructions"
]
df = df[required_columns]

# Clean the data
print("[INFO] Cleaning data...")
# Storing the names of the items which are dropped by dropna
dropped_names = df[df['name'].isnull() | df['ingredients'].isnull() | df['instructions'].isnull()]['name'].dropna().tolist()
if dropped_names:
    output_path = 'dropped_recipes.txt'
    print(f"[INFO] Dropping {len(dropped_names)} recipes with missing data. Their names are saved to '{output_path}'.")
    with open(output_path, "w", encoding="utf-8") as f:
        for name in dropped_names:
            f.write(f"{name}\n")
df = df.dropna(subset=["name", "ingredients", "instructions"])  # remove rows missing key fields
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)  # strip whitespace
df["name"] = df["name"].str.lower()  # normalize dish names for matching


# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
print(f"[SUCCESS] Cleaned dataset saved to {OUTPUT_FILE}")
print(f"[INFO] Total recipes: {len(df)}")
