"""
03_visualizations.py
Generates the five key charts for the Superstore sales analysis project:
monthly trend, category, region, top sub-categories, and customer
concentration (Pareto). Uses a consistent navy/slate theme with an
amber accent color throughout, for a cohesive visual identity.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# --- Consistent theme ---
NAVY = '#1F3A5F'
SLATE = '#4C6B8A'
ACCENT = '#D98E04'
GREY = '#8C99A6'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.edgecolor': '#333333',
    'axes.labelcolor': '#333333',
    'text.color': '#222222',
    'xtick.color': '#333333',
    'ytick.color': '#333333',
    'axes.titleweight': 'bold',
    'axes.titlesize': 14,
    'axes.titlepad': 12,
})
plt.style.use('seaborn-v0_8-whitegrid')


def style_axis(ax):
    """Remove top/right border for a cleaner look, consistent across all charts."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


df = pd.read_csv("data/processed/superstore_clean.csv")

# 1. Monthly sales trend
monthly = df.groupby("Month")["Sales"].sum()
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly.index, monthly.values, marker='o', markersize=3, linewidth=2, color=NAVY)
ax.set_title("Monthly Sales Trend (2015-2018)")
ax.set_xlabel("Month")
ax.set_ylabel("Sales ($)")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ticks = monthly.index[::3]
ax.set_xticks(ticks)
ax.set_xticklabels(ticks, rotation=45, ha='right')
style_axis(ax)
plt.tight_layout()
plt.savefig("outputs/1_monthly_sales_trend.png", dpi=150)
plt.close()

# 2. Sales by Category
cat = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(cat.index, cat.values, color=[NAVY, SLATE, GREY])
ax.set_title("Total Sales by Category")
ax.set_ylabel("Sales ($)")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for b in bars:
    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), f'${b.get_height():,.0f}',
            ha='center', va='bottom', fontsize=9)
style_axis(ax)
plt.tight_layout()
plt.savefig("outputs/2_sales_by_category.png", dpi=150)
plt.close()

# 3. Sales by Region
reg = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(reg.index, reg.values, color=[NAVY, SLATE, SLATE, GREY])
ax.set_title("Total Sales by Region")
ax.set_ylabel("Sales ($)")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for b in bars:
    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), f'${b.get_height():,.0f}',
            ha='center', va='bottom', fontsize=9)
style_axis(ax)
plt.tight_layout()
plt.savefig("outputs/3_sales_by_region.png", dpi=150)
plt.close()

# 4. Top 10 Sub-Categories
subcat = df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(subcat.index[::-1], subcat.values[::-1], color=NAVY)
ax.set_title("Top 10 Sub-Categories by Sales")
ax.set_xlabel("Sales ($)")
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
style_axis(ax)
plt.tight_layout()
plt.savefig("outputs/4_top_subcategories.png", dpi=150)
plt.close()

# 5. Pareto chart: customer concentration
cust_sales = df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).reset_index()
cust_sales["cum_pct"] = cust_sales["Sales"].cumsum() / cust_sales["Sales"].sum() * 100
cust_sales["customer_pct"] = (cust_sales.index + 1) / len(cust_sales) * 100

fig, ax1 = plt.subplots(figsize=(9, 5))
ax1.plot(cust_sales["customer_pct"], cust_sales["cum_pct"], color=NAVY, linewidth=2.5)
ax1.axvline(10, color=ACCENT, linestyle='--', linewidth=1.5)
cutoff_row = (cust_sales["customer_pct"] - 10).abs().idxmin()
ax1.axhline(cust_sales.loc[cutoff_row, "cum_pct"], color=ACCENT, linestyle='--', linewidth=1.5)
ax1.set_title("Customer Sales Concentration (Pareto Curve)")
ax1.set_xlabel("Percent of Customers (ranked by sales)")
ax1.set_ylabel("Cumulative Percent of Sales")
ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.0f}%'))
ax1.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.0f}%'))
style_axis(ax1)
plt.tight_layout()
plt.savefig("outputs/5_customer_concentration_pareto.png", dpi=150)
plt.close()

print("All 5 charts saved to outputs/ with consistent navy/slate theme")
