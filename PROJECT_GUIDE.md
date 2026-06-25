# Brazilian E-Commerce Analytics — A Beginner's Data Engineering & Analysis Project

> A complete, follow-along project that takes you through the **entire data science process** — from raw messy files to a clean database to real insights — using only free tools (Anaconda + Kaggle).
>
> By the end you'll have a portfolio project on GitHub that shows you can **engineer** data (clean it, join it, load it into a database) and **analyze** it (explore it, visualize it, draw conclusions). These are the two skills employers actually hire for.

---

## Table of contents

1. [Why this project](#0-why-this-project)
2. [Step 1 — Understand the data science process](#step-1--understand-the-data-science-process)
3. [Step 2 — Set up your tools (Anaconda)](#step-2--set-up-your-tools-anaconda)
4. [Step 3 — Define the problem](#step-3--define-the-problem)
5. [Step 4 — Get the data (Kaggle)](#step-4--get-the-data-kaggle)
6. [Step 5 — Understand the data](#step-5--understand-the-data)
7. [Step 6 — Clean the data](#step-6--clean-the-data)
8. [Step 7 — Engineer the data (the ETL core)](#step-7--engineer-the-data-the-etl-core)
9. [Step 8 — Load into a database (SQLite)](#step-8--load-into-a-database-sqlite)
10. [Step 9 — Exploratory Data Analysis (EDA)](#step-9--exploratory-data-analysis-eda)
11. [Step 10 — Answer the business questions with visualizations](#step-10--answer-the-business-questions-with-visualizations)
12. [Step 11 — Write up your insights](#step-11--write-up-your-insights)
13. [Step 12 — Publish to GitHub](#step-12--publish-to-github)
14. [Where to go next](#where-to-go-next)

---

## 0. Why this project

Most beginner tutorials hand you one already-clean CSV and jump straight to charts. That skips the part that **is the job**: taking messy, scattered, real-world data and turning it into something usable. That's **data engineering**, and it's exactly what you said you want to focus on.

The dataset we'll use — Olist's Brazilian e-commerce data — comes as **9 separate files** that have to be joined together correctly before you can analyze anything. That makes it perfect: you'll practice the engineering skills (joining tables, fixing data types, handling missing values, loading into a database) *and* the analysis skills (exploring, visualizing, concluding) in one project.

**You do not need prior skills.** Every line of code is explained. If you can copy, paste, and read carefully, you can do this.

---

## Step 1 — Understand the data science process

Before touching code, hold the whole map in your head. Almost every data project follows these stages, and we'll hit each one:

| Stage | What it means | Where we do it |
|-------|---------------|----------------|
| **1. Define the problem** | Decide what questions you're answering | Step 3 |
| **2. Acquire data** | Get the raw data | Step 4 |
| **3. Understand data** | Look at what you have, learn its shape | Step 5 |
| **4. Clean data** | Fix missing values, wrong types, duplicates | Step 6 |
| **5. Engineer / integrate** | Combine sources into one usable dataset | Steps 7–8 |
| **6. Explore (EDA)** | Find patterns, distributions, oddities | Step 9 |
| **7. Analyze & visualize** | Answer your questions | Step 10 |
| **8. Communicate** | Explain what you found | Step 11 |

A useful mental model: **80% of real data work is stages 2–5** (getting and preparing data). The pretty charts are the last 20%. This project deliberately spends most of its time where the real work is.

---

## Step 2 — Set up your tools (Anaconda)

You already have Anaconda — good. Anaconda is a bundle that includes Python plus the data libraries and a tool called **conda** for managing them. We'll create an isolated "environment" so this project's tools never conflict with anything else on your computer.

### 2.1 Open the terminal

- **Windows:** open **Anaconda Prompt** (search for it in the Start menu).
- **Mac/Linux:** open the **Terminal** app.

### 2.2 Create a dedicated environment

Copy these one line at a time. A line starting with `#` is a comment — you don't type those.

```bash
# Create a new environment called "ecommerce" with Python 3.11
conda create -n ecommerce python=3.11 -y

# Activate it (you must do this every time you work on the project)
conda activate ecommerce
```

> **What just happened?** An *environment* is a private sandbox of Python and libraries. When you see `(ecommerce)` at the start of your terminal line, you're inside it. This is a professional habit — every project gets its own environment so versions never clash.

### 2.3 Install the libraries we'll use

```bash
conda install -y pandas numpy matplotlib seaborn jupyter
pip install kaggle
```

What each one does:

- **pandas** — the workhorse. Loads tables, cleans, joins, transforms. This is 90% of the job.
- **numpy** — fast math under the hood (pandas uses it).
- **matplotlib** — the base plotting library.
- **seaborn** — prettier charts with less code, built on matplotlib.
- **jupyter** — the notebook interface where you'll write and run code in small chunks.
- **kaggle** — a command-line tool to download datasets from Kaggle.

### 2.4 Set up the project folder

Create a folder and the structure below. You can do this in your file explorer, or in the terminal:

```bash
# Go to wherever you keep projects, e.g. your home folder
cd ~

# Make the project folder and subfolders
mkdir -p brazilian-ecommerce-analysis/data/raw
mkdir -p brazilian-ecommerce-analysis/data/processed
mkdir -p brazilian-ecommerce-analysis/notebooks
mkdir -p brazilian-ecommerce-analysis/reports/figures
cd brazilian-ecommerce-analysis
```

Your structure:

```
brazilian-ecommerce-analysis/
├── data/
│   ├── raw/          ← original downloaded files (never edit these)
│   └── processed/    ← cleaned data you create
├── notebooks/        ← your Jupyter notebooks
└── reports/
    └── figures/      ← saved charts
```

> **Why separate `raw` from `processed`?** A golden rule of data engineering: **never modify your raw data**. You always keep an untouched copy so that if you make a mistake, you can re-run your pipeline from the original. Your cleaned outputs go in `processed/`.

### 2.5 Launch Jupyter

```bash
jupyter notebook
```

This opens a tab in your web browser. Navigate into the `notebooks` folder and create a new notebook (**New → Python 3**). Rename it `01_understanding.ipynb`. You'll write code in "cells" and run each with **Shift + Enter**.

---

## Step 3 — Define the problem

Data work without a question is just aimless wrangling. Imagine you're a junior analyst at Olist (a real Brazilian online marketplace). Leadership asks:

> **"How is our business doing, and what's hurting customer satisfaction?"**

We'll break that vague ask into concrete, answerable questions:

1. **Sales over time** — Is the business growing? Are there seasonal patterns?
2. **Geography** — Which states drive the most revenue?
3. **Delivery performance** — How long do deliveries take, and do late deliveries hurt review scores?
4. **Product categories** — Which categories sell the most and which earn the best reviews?
5. **Payments** — How do customers pay, and do installment plans relate to order size?

Writing questions down *first* keeps you focused. Every chart you make later should answer one of these.

---

## Step 4 — Get the data (Kaggle)

The dataset is **"Brazilian E-Commerce Public Dataset by Olist"**. There are two ways to get it.

### Option A — Manual download (simplest, do this if unsure)

1. Go to: `https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce`
2. Click **Download** (you'll need a free Kaggle account).
3. Unzip the downloaded file.
4. Move all the `.csv` files into your project's `data/raw/` folder.

### Option B — Kaggle API (the "engineer" way, fully automated)

1. On Kaggle, click your profile picture → **Settings** → **API** → **Create New Token**. This downloads `kaggle.json`.
2. Place it where the tool expects:
   - **Mac/Linux:** `~/.kaggle/kaggle.json`
   - **Windows:** `C:\Users\<YourName>\.kaggle\kaggle.json`
3. Then run:

```bash
# From inside your project folder
kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw --unzip
```

> **Why automate it?** In real jobs, data refreshes regularly. A scripted download means you can re-pull fresh data with one command instead of clicking around. That repeatability *is* data engineering.

### What you should now have

Nine CSV files in `data/raw/`:

```
olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

These nine tables are **relational** — they connect to each other through shared ID columns (like `order_id` and `customer_id`), just like tables in a real database. Joining them is the heart of this project.

---

## Step 5 — Understand the data

Open your `01_understanding.ipynb` notebook. We'll load each file and look at it. **Never start cleaning before you understand what you have.**

```python
# Import the libraries. The "as pd" gives pandas a short nickname.
import pandas as pd
import numpy as np

# Tell pandas to show all columns when we print a table
pd.set_option("display.max_columns", None)

# A helper path so we don't retype the folder every time
RAW = "../data/raw/"   # ".." means "go up one folder" (out of notebooks/)
```

> **Note on the path:** your notebook lives in `notebooks/`, but the data lives in `data/raw/`. `../data/raw/` means "go up one level, then into data/raw". If you get a "file not found" error, this path is the usual culprit.

### 5.1 Load every table

```python
# Read each CSV into a pandas DataFrame (a table in memory)
customers   = pd.read_csv(RAW + "olist_customers_dataset.csv")
orders      = pd.read_csv(RAW + "olist_orders_dataset.csv")
order_items = pd.read_csv(RAW + "olist_order_items_dataset.csv")
payments    = pd.read_csv(RAW + "olist_order_payments_dataset.csv")
reviews     = pd.read_csv(RAW + "olist_order_reviews_dataset.csv")
products    = pd.read_csv(RAW + "olist_products_dataset.csv")
sellers     = pd.read_csv(RAW + "olist_sellers_dataset.csv")
geolocation = pd.read_csv(RAW + "olist_geolocation_dataset.csv")
translation = pd.read_csv(RAW + "product_category_name_translation.csv")

print("All files loaded successfully!")
```

A **DataFrame** is pandas' name for a table — rows and columns, like a spreadsheet you can manipulate with code.

### 5.2 Look at the main orders table

```python
# .head() shows the first 5 rows
orders.head()
```

```python
# .shape tells you (number of rows, number of columns)
print("Orders shape:", orders.shape)

# .info() shows column names, how many non-empty values, and data types
orders.info()
```

Read the output carefully. You'll notice the date columns (like `order_purchase_timestamp`) show up as type `object` — that means pandas is treating them as plain **text**, not real dates. We'll fix that in cleaning. Spotting this now is exactly the "understanding" step doing its job.

### 5.3 Understand how the tables connect

This is the most important diagram in the whole project. The tables link through shared keys:

```
                    ┌─────────────┐
                    │  customers  │
                    │ customer_id │
                    └──────┬──────┘
                           │ customer_id
                    ┌──────┴──────┐
                    │   orders    │
                    │  order_id   │
                    └──────┬──────┘
          ┌────────────────┼────────────────┐
   order_id │         order_id │       order_id │
   ┌────────┴───┐   ┌──────────┴──┐   ┌────────┴────┐
   │order_items │   │  payments   │   │   reviews   │
   └────┬───────┘   └─────────────┘   └─────────────┘
        │ product_id
   ┌────┴─────┐
   │ products │
   └────┬─────┘
        │ product_category_name
   ┌────┴────────┐
   │ translation │  (Portuguese → English category names)
   └─────────────┘
```

In plain words:

- A **customer** places **orders**.
- Each **order** contains one or more **order_items** (the actual products bought).
- Each order has **payments** and **reviews**.
- Each item points to a **product**, and each product has a **category** we can translate to English.

When you can read a diagram like this, you understand the data. Sketch it on paper — it'll make the next steps click.

### 5.4 Check the other tables quickly

```python
# Look at a couple of rows from each to build intuition
for name, df in [("order_items", order_items), ("payments", payments),
                 ("reviews", reviews), ("products", products)]:
    print(f"\n===== {name} | shape {df.shape} =====")
    display(df.head(2))
```

> `display()` is a Jupyter helper that prints tables nicely. `print()` works too but looks plainer.

---

## Step 6 — Clean the data

Now we fix problems. We'll clean each table, then save the cleaned versions. **Cleaning is iterative** — you'll often spot new issues and come back. That's normal.

Create a new notebook: `02_cleaning.ipynb`. Re-run the import and load cells from Step 5 at the top (notebooks don't remember each other).

### 6.1 Convert text into real dates

Right now date columns are text, so you can't do math like "days between purchase and delivery". Let's fix the `orders` table.

```python
# These columns hold dates but are stored as text
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

# Convert each one to a real datetime type.
# errors="coerce" turns anything unparseable into NaT (a "missing date"),
# which is safer than crashing.
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

orders.info()  # the date columns should now say datetime64
```

> **Why this matters:** once these are real dates, pandas can subtract them, extract the month, sort by them, and group by year. As text, none of that works. Converting types correctly is a foundational engineering skill.

### 6.2 Find missing values

```python
# Count missing values per column, and show as a percentage
missing = orders.isnull().sum()
missing_pct = (missing / len(orders) * 100).round(2)
pd.DataFrame({"missing_count": missing, "missing_pct": missing_pct})
```

You'll see some orders are missing a `order_delivered_customer_date`. That's not corrupt data — those are orders that were cancelled or not yet delivered. **Understanding *why* data is missing tells you how to handle it.** Here, we'll keep those rows but be careful: when we measure delivery time later, we'll only count orders that actually have a delivery date.

### 6.3 Handle missing values in products

```python
# Some products are missing their category name
print("Missing categories:", products["product_category_name"].isnull().sum())

# Fill missing category names with the label "unknown" so they don't
# silently disappear when we group later.
products["product_category_name"] = products["product_category_name"].fillna("unknown")
```

> **Decision-making, not rote rules:** there's no single "right" way to handle missing data. You can drop rows, fill them with a default, or fill with a statistic (like the average). Here "unknown" is honest — we're not inventing a category, just labelling the gap. Document choices like this; interviewers love to see reasoning.

### 6.4 Remove duplicates

```python
# Check for fully duplicated rows in each key table
for name, df in [("orders", orders), ("order_items", order_items),
                 ("payments", payments), ("customers", customers)]:
    dupes = df.duplicated().sum()
    print(f"{name}: {dupes} duplicate rows")
```

If any show duplicates, remove them with `df = df.drop_duplicates()`. Duplicates inflate counts and skew averages, so this is a routine safety check.

### 6.5 Translate product categories to English

The category names are in Portuguese. The `translation` table maps them to English — a tiny taste of joining, which we'll do at scale next.

```python
# Merge English names onto the products table using the shared category column
products = products.merge(translation, on="product_category_name", how="left")

# For any category with no translation, fall back to the original name
products["product_category_name_english"] = (
    products["product_category_name_english"].fillna(products["product_category_name"])
)

products[["product_category_name", "product_category_name_english"]].head()
```

> **`merge` is the single most important pandas skill for data engineering.** It's the same idea as a SQL JOIN: line up two tables on a shared column and stitch them together. `how="left"` means "keep every product row, and attach a translation where one exists." We'll lean on this heavily in the next step.

---

## Step 7 — Engineer the data (the ETL core)

This is the centerpiece. We'll combine the separate tables into **one analytical table** where each row is an order item enriched with everything we know about it — the customer, the product, the timing. This single wide table is what makes analysis easy.

This pattern — **Extract** (load files), **Transform** (clean + join), **Load** (save the result) — is called **ETL**, and it's the core of most data engineering jobs.

Create `03_engineering.ipynb`. Load the data and re-apply the cleaning from Step 6 first (or, better, see the note at the end about turning this into a reusable script).

### 7.1 Build the master table with a chain of joins

```python
# Start from order_items — the most granular table (one row per product per order)
df = order_items.copy()

# 1) Attach order-level info (status, dates) via order_id
df = df.merge(orders, on="order_id", how="left")

# 2) Attach customer info (state, city) via customer_id
df = df.merge(customers, on="customer_id", how="left")

# 3) Attach product info (category, weight) via product_id
df = df.merge(products, on="product_id", how="left")

print("Master table shape:", df.shape)
df.head(2)
```

Read what each line does: we keep adding columns from other tables, matched up by shared IDs. After this, a single row tells you *what* was bought, *who* bought it, *where* they are, and *when* it happened — all in one place.

> **Why `how="left"` everywhere?** We always keep every row from `order_items` (our base) and attach matching info from the right-hand table. A "left join" never drops base rows — it just fills attached columns with blanks when there's no match. This protects you from accidentally losing data during joins, a very common beginner bug.

### 7.2 Bring in review scores

Reviews are at the *order* level (one review per order), while our table is at the *item* level. We summarize reviews to one score per order first, then join.

```python
# Some orders have more than one review row; take the average score per order
review_scores = reviews.groupby("order_id")["review_score"].mean().reset_index()

# Attach the score to our master table
df = df.merge(review_scores, on="order_id", how="left")
```

> **`groupby` explained:** it splits the data into groups (here, one group per `order_id`), applies a calculation to each group (here, the mean score), and combines the results. Group-summarize-join is one of the most common moves in all of data work.

### 7.3 Engineer new features

"Feature engineering" means creating new, more useful columns from existing ones. This is where domain thinking turns raw fields into insight.

```python
# Total a customer paid for this item (product price + shipping)
df["total_value"] = df["price"] + df["freight_value"]

# How many days the delivery actually took
df["delivery_days"] = (
    df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
).dt.days

# How many days early/late vs. the estimate
# Positive = delivered earlier than promised; negative = late
df["delivery_vs_estimate"] = (
    df["order_estimated_delivery_date"] - df["order_delivered_customer_date"]
).dt.days

# A simple flag: was this delivery late?
df["is_late"] = df["delivery_vs_estimate"] < 0

# Pull the year and month out of the purchase date for trend analysis
df["purchase_year"]  = df["order_purchase_timestamp"].dt.year
df["purchase_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

df[["total_value", "delivery_days", "delivery_vs_estimate", "is_late",
    "purchase_month"]].head()
```

Each of these new columns directly serves a question from Step 3. `delivery_days` and `is_late` will answer the delivery-performance question; `purchase_month` powers the sales-trend chart. **Good features come from your questions, not the other way around.**

### 7.4 Final filter and save

```python
# Focus on completed orders for a clean analysis of the "normal" business
df_clean = df[df["order_status"] == "delivered"].copy()

print("Rows before filter:", len(df))
print("Rows after keeping only delivered orders:", len(df_clean))

# Save the engineered table so we never have to rebuild it from scratch
df_clean.to_csv("../data/processed/ecommerce_clean.csv", index=False)
print("Saved to data/processed/ecommerce_clean.csv")
```

You now have a single, clean, analysis-ready file. **This file is the product of your data engineering work** — and it's the thing that makes the analysis steps short and easy.

---

## Step 8 — Load into a database (SQLite)

Real companies don't pass CSVs around — they store data in **databases** and query it with **SQL**. SQLite is a tiny database built into Python (nothing to install), so it's the perfect place to learn. This step makes your project notably more impressive on GitHub because it shows you understand databases and SQL, not just pandas.

```python
import sqlite3

# Create (or open) a database file
conn = sqlite3.connect("../data/processed/ecommerce.db")

# Write our clean DataFrame into a table called "orders_clean"
df_clean.to_sql("orders_clean", conn, if_exists="replace", index=False)

print("Data loaded into SQLite database.")
```

Now query it with **SQL**, the universal language of data:

```python
# Top 5 states by total revenue, using SQL
query = """
SELECT customer_state,
       ROUND(SUM(total_value), 2) AS revenue,
       COUNT(*)                   AS num_items
FROM orders_clean
GROUP BY customer_state
ORDER BY revenue DESC
LIMIT 5
"""

pd.read_sql_query(query, conn)
```

Read the SQL like a sentence: *select* the state, the summed value, and a count; *from* our table; *group by* state; *order* by revenue, highest first; *limit* to 5. SQL is one of the most in-demand data skills, and you just used it on your own data.

```python
# Always close the connection when done
conn.close()
```

> **pandas vs. SQL — when to use which?** They do overlapping things. SQL shines for pulling and aggregating data *from* a database; pandas shines for flexible in-memory manipulation and plotting. Knowing both, and showing both in one project, is exactly what makes a portfolio piece stand out.

---

## Step 9 — Exploratory Data Analysis (EDA)

EDA means getting to know your prepared data through summaries and quick plots before drawing conclusions. Create `04_analysis.ipynb` and load your clean file:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")  # nicer default chart styling

df = pd.read_csv("../data/processed/ecommerce_clean.csv")
print("Loaded clean data:", df.shape)
```

### 9.1 Summary statistics

```python
# .describe() gives count, mean, min, max, and quartiles for numeric columns
df[["price", "freight_value", "total_value",
    "delivery_days", "review_score"]].describe()
```

Look for things that seem off — a maximum price that's enormous, negative delivery days (impossible), etc. EDA is detective work: every surprising number is a clue worth chasing.

### 9.2 Distributions

```python
# How long do deliveries take? A histogram shows the spread.
plt.figure(figsize=(10, 5))
sns.histplot(df["delivery_days"].dropna(), bins=50)
plt.title("Distribution of Delivery Times")
plt.xlabel("Days to deliver")
plt.ylabel("Number of orders")
plt.show()
```

You'll likely see most deliveries cluster in the 1–2 week range with a long tail of slow ones. Understanding that **shape** (where the bulk sits, how long the tail is) matters more than any single average.

```python
# How are review scores distributed?
plt.figure(figsize=(8, 5))
sns.countplot(x="review_score", data=df)
plt.title("Distribution of Review Scores")
plt.xlabel("Review score (1–5)")
plt.ylabel("Count")
plt.show()
```

---

## Step 10 — Answer the business questions with visualizations

Now we deliberately answer each question from Step 3. We'll also **save each chart** to `reports/figures/` so they can appear in your GitHub README.

### Q1 — Are sales growing over time?

```python
# Total revenue per month
monthly = (df.groupby("purchase_month")["total_value"]
             .sum()
             .reset_index()
             .sort_values("purchase_month"))

plt.figure(figsize=(13, 5))
plt.plot(monthly["purchase_month"], monthly["total_value"], marker="o")
plt.title("Monthly Revenue Over Time")
plt.xlabel("Month")
plt.ylabel("Revenue (BRL)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../reports/figures/monthly_revenue.png", dpi=150)
plt.show()
```

> `plt.savefig(...)` writes the chart to a file. `dpi=150` makes it sharp. `tight_layout()` stops labels from being cut off. Saving figures is what lets you embed them in your README later.

### Q2 — Which states drive revenue?

```python
top_states = (df.groupby("customer_state")["total_value"]
                .sum()
                .sort_values(ascending=False)
                .head(10))

plt.figure(figsize=(11, 5))
sns.barplot(x=top_states.index, y=top_states.values)
plt.title("Top 10 States by Revenue")
plt.xlabel("State")
plt.ylabel("Revenue (BRL)")
plt.tight_layout()
plt.savefig("../reports/figures/revenue_by_state.png", dpi=150)
plt.show()
```

You'll find São Paulo (SP) dominates — a real, useful business fact about where the customer base concentrates.

### Q3 — Do late deliveries hurt reviews?

This is the most interesting question because it links two things and tests a hypothesis.

```python
# Average review score for on-time vs. late deliveries
late_impact = df.groupby("is_late")["review_score"].mean()

plt.figure(figsize=(7, 5))
sns.barplot(x=["On Time", "Late"], y=late_impact.values)
plt.title("Average Review Score: On-Time vs. Late Deliveries")
plt.ylabel("Average review score")
plt.ylim(0, 5)
plt.tight_layout()
plt.savefig("../reports/figures/late_vs_reviews.png", dpi=150)
plt.show()

print(late_impact)
```

You'll almost certainly see late deliveries score much lower. That's an **actionable insight**: improving delivery reliability would directly raise satisfaction. This is the kind of finding that makes a portfolio project feel like real analysis instead of a coding exercise.

### Q4 — Which product categories perform best?

```python
# Top 10 categories by number of items sold
top_cats = (df["product_category_name_english"]
              .value_counts()
              .head(10))

plt.figure(figsize=(11, 6))
sns.barplot(y=top_cats.index, x=top_cats.values)
plt.title("Top 10 Product Categories by Items Sold")
plt.xlabel("Items sold")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig("../reports/figures/top_categories.png", dpi=150)
plt.show()
```

### Q5 — How do customers pay?

```python
# We need the payments table for this; load and merge payment types
payments = pd.read_csv("../data/raw/olist_order_payments_dataset.csv")
pay_counts = payments["payment_type"].value_counts()

plt.figure(figsize=(8, 5))
plt.pie(pay_counts.values, labels=pay_counts.index, autopct="%1.1f%%",
        startangle=90)
plt.title("Payment Method Breakdown")
plt.tight_layout()
plt.savefig("../reports/figures/payment_methods.png", dpi=150)
plt.show()
```

In Brazil you'll see credit card dominate, with "boleto" (a popular Brazilian bank slip) second — a nice culturally-specific detail to mention in your write-up.

---

## Step 11 — Write up your insights

A project nobody can understand has no value. Translate your charts into plain-English findings. Here's a template — replace the bracketed bits with what *your* charts actually show:

> **Key findings**
> 1. **Growth:** Revenue grew steadily from [start] through [end], with a visible spike around [month] (likely a Black Friday effect).
> 2. **Geography:** Revenue is heavily concentrated in [top state], which alone accounts for roughly [X]% of sales — suggesting expansion opportunity in under-served states.
> 3. **Delivery → satisfaction:** Late deliveries averaged [X] stars versus [Y] for on-time ones. Delivery reliability is the clearest lever for improving customer satisfaction.
> 4. **Product mix:** The top categories were [list]. Marketing and inventory should prioritize these.
> 5. **Payments:** [X]% of customers paid by credit card; installment plans were common on larger orders.

Notice each finding ties back to a Step 3 question and suggests a *business action*. That's the difference between "I made charts" and "I delivered analysis."

---

## Step 12 — Publish to GitHub

This turns your work into a portfolio piece. GitHub is where employers look.

### 12.1 Files included in this project

Alongside this guide you've been given four ready-to-use files. Put them in your project's root folder:

- **`README.md`** — the front page of your repo (edit in your findings and chart images).
- **`requirements.txt`** — lists the Python packages so others can reproduce your setup.
- **`environment.yml`** — the conda version of the same thing.
- **`.gitignore`** — tells Git which files *not* to upload (like the big raw data).

> **Why ignore the raw data?** Raw datasets are often large and aren't yours to redistribute. The professional convention is to *not* commit raw data, and instead document in the README how to download it (which you did in Step 4). Your `.gitignore` already excludes `data/raw/`.

### 12.2 Put it on GitHub

First, make a free account at github.com and install Git (`conda install -y git` works). Then, from your project folder:

```bash
# Turn the folder into a Git repository
git init

# Stage all files (gitignore decides what's excluded)
git add .

# Save a snapshot with a message
git commit -m "Initial commit: Brazilian e-commerce analysis pipeline"
```

Now create an empty repository on github.com (click **New**, name it `brazilian-ecommerce-analysis`, don't add a README since you have one). Then connect and push:

```bash
# Link your local folder to the GitHub repo (use the URL GitHub shows you)
git remote add origin https://github.com/YOUR_USERNAME/brazilian-ecommerce-analysis.git

# Rename your branch to "main" (GitHub's default)
git branch -M main

# Upload everything
git push -u origin main
```

Refresh the GitHub page — your project is live. To embed a chart in your README, add a line like:

```markdown
![Monthly Revenue](reports/figures/monthly_revenue.png)
```

(Charts in `reports/figures/` *are* committed, unlike raw data — that's intentional, so they display in your README.)

### 12.3 What makes this repo impressive

When someone lands on your repo, they'll see, in order: a clear README explaining the business problem, charts with real insights, a clean folder structure, multiple notebooks showing each stage, **and** evidence you used pandas, SQL, and a database. That combination — engineering *and* analysis, clearly communicated — is exactly what a junior data role looks for.

---

## Bonus — Turn your cleaning into a reusable script

Notebooks are great for exploring, but engineers package repeatable work into scripts. Once everything works, copy your cleaning + joining code into `src/pipeline.py` as a function:

```python
# src/pipeline.py
import pandas as pd

def build_clean_dataset(raw_path="data/raw/", out_path="data/processed/"):
    """Load raw Olist files, clean, join, and save one analytical table."""
    # ... (paste your loading, cleaning, and joining code here) ...
    # df_clean.to_csv(out_path + "ecommerce_clean.csv", index=False)
    # return df_clean

if __name__ == "__main__":
    build_clean_dataset()
    print("Pipeline complete.")
```

Then you can rebuild your entire clean dataset anytime with one command:

```bash
python src/pipeline.py
```

That one move — wrapping your work in a function you can re-run — is the mindset shift from "someone who writes data code" to "data engineer." Add it to your README and you've genuinely leveled up.

---

## Where to go next

Once this is solid, here are natural next projects that build on what you learned:

- **Add a simple prediction:** can you predict review score from delivery time and price? (Intro to machine learning with `scikit-learn`.)
- **Automate the pipeline:** schedule your `pipeline.py` to run on new data.
- **Build a dashboard:** turn your charts into an interactive app with `streamlit` (about 30 lines of code).
- **Go bigger:** try a larger dataset where pandas struggles, and learn tools like DuckDB or PySpark.

You now have the full loop — define, acquire, understand, clean, engineer, store, analyze, communicate, publish. That loop is the job. Repeat it on datasets you find interesting, and your skills (and portfolio) compound fast.

**Good luck — and commit early, commit often.**
