"""
pipeline.py — Reusable ETL for the Brazilian E-Commerce project.

Run from the project root with:
    python src/pipeline.py

It loads the 9 raw Olist CSVs, cleans and joins them into a single
analysis-ready table, and saves it to data/processed/ecommerce_clean.csv
(and into a SQLite database). This is the "engineer" version of the
notebook work — one command rebuilds everything from the raw files.
"""

import pandas as pd
import sqlite3
from pathlib import Path


def build_clean_dataset(raw_path="data/raw/", out_path="data/processed/"):
    raw = Path(raw_path)
    out = Path(out_path)
    out.mkdir(parents=True, exist_ok=True)

    # ---- EXTRACT: load every raw file ----
    customers   = pd.read_csv(raw / "olist_customers_dataset.csv")
    orders      = pd.read_csv(raw / "olist_orders_dataset.csv")
    order_items = pd.read_csv(raw / "olist_order_items_dataset.csv")
    reviews     = pd.read_csv(raw / "olist_order_reviews_dataset.csv")
    products    = pd.read_csv(raw / "olist_products_dataset.csv")
    translation = pd.read_csv(raw / "product_category_name_translation.csv")

    # ---- TRANSFORM: clean ----
    date_cols = [
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    products["product_category_name"] = (
        products["product_category_name"].fillna("unknown")
    )
    products = products.merge(translation, on="product_category_name", how="left")
    products["product_category_name_english"] = (
        products["product_category_name_english"]
        .fillna(products["product_category_name"])
    )

    # ---- TRANSFORM: join into one master table ----
    df = order_items.copy()
    df = df.merge(orders, on="order_id", how="left")
    df = df.merge(customers, on="customer_id", how="left")
    df = df.merge(products, on="product_id", how="left")

    review_scores = (
        reviews.groupby("order_id")["review_score"].mean().reset_index()
    )
    df = df.merge(review_scores, on="order_id", how="left")

    # ---- TRANSFORM: engineer features ----
    df["total_value"] = df["price"] + df["freight_value"]
    df["delivery_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days
    df["delivery_vs_estimate"] = (
        df["order_estimated_delivery_date"] - df["order_delivered_customer_date"]
    ).dt.days
    df["is_late"] = df["delivery_vs_estimate"] < 0
    df["purchase_year"] = df["order_purchase_timestamp"].dt.year
    df["purchase_month"] = (
        df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    )

    df_clean = df[df["order_status"] == "delivered"].copy()

    # ---- LOAD: save outputs ----
    csv_out = out / "ecommerce_clean.csv"
    df_clean.to_csv(csv_out, index=False)

    conn = sqlite3.connect(out / "ecommerce.db")
    df_clean.to_sql("orders_clean", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Pipeline complete. {len(df_clean):,} rows saved to {csv_out}")
    return df_clean


if __name__ == "__main__":
    build_clean_dataset()
