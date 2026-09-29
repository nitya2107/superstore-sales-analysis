"""
02_exploratory_analysis.py
Explores the cleaned Superstore dataset: sales by category, region,
segment, sub-category, monthly trend, and customer concentration.
"""

import pandas as pd

pd.set_option('display.float_format', lambda x: f'{x:,.0f}')

df = pd.read_csv("data/processed/superstore_clean.csv")

# Sales by Category
print("Sales by Category:")
print(df.groupby("Category")["Sales"].sum().sort_values(ascending=False), "\n")

# Sales by Region
print("Sales by Region:")
print(df.groupby("Region")["Sales"].sum().sort_values(ascending=False), "\n")

# Sales by Segment
print("Sales by Segment:")
print(df.groupby("Segment")["Sales"].sum().sort_values(ascending=False), "\n")

# Top 10 Sub-Categories
print("Top 10 Sub-Categories:")
print(df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).head(10), "\n")

# Yearly sales and year-over-year growth
yearly = df.groupby("Year")["Sales"].sum()
print("Yearly Sales:")
print(yearly)
print("\nYear-over-Year Growth %:")
print((yearly.pct_change() * 100).round(1), "\n")

# Monthly trend - best and worst month
monthly = df.groupby("Month")["Sales"].sum()
print(f"Best month: {monthly.idxmax()} (${monthly.max():,.0f})")
print(f"Worst month: {monthly.idxmin()} (${monthly.min():,.0f})\n")

# Customer concentration
cust_sales = df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False)
total_sales = df["Sales"].sum()
top10_share = cust_sales.head(10).sum() / total_sales * 100
n_top10pct = int(len(cust_sales) * 0.10)
top10pct_share = cust_sales.head(n_top10pct).sum() / total_sales * 100

print(f"Top 10 customers make up {top10_share:.1f}% of total sales")
print(f"Top 10% of customers ({n_top10pct} people) make up {top10pct_share:.1f}% of total sales")
print(f"Total unique customers: {len(cust_sales)}")
