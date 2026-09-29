"""
01_data_cleaning.py
Cleans the raw Superstore sales dataset: fixes date formats,
checks duplicates, and engineers helper columns for analysis.
"""

import pandas as pd

# Load raw data
df = pd.read_csv("data/raw/train.csv", encoding="latin-1")

# Parse dates (file uses day/month/year format)
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d/%m/%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d/%m/%Y")

# Check for duplicate Order ID + Product ID combinations
dupes = df[df.duplicated(["Order ID", "Product ID"], keep=False)]
print(f"Found {len(dupes)} rows involved in Order ID + Product ID duplicates")
print(dupes.sort_values(["Order ID", "Product ID"])[
    ["Order ID", "Product ID", "Product Name", "Sales"]])

# Engineer helper columns
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
df["Ship Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

# Save cleaned dataset
df.to_csv("data/processed/superstore_clean.csv", index=False)
print("Cleaned data saved to data/processed/superstore_clean.csv")
print(f"Final shape: {df.shape}")
