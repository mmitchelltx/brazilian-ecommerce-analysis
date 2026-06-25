# Brazilian E-Commerce Analytics 🇧🇷

An end-to-end **data engineering and analysis** project built on Olist's public Brazilian e-commerce dataset. This repo takes raw, multi-table data through a full pipeline — clean, join, load into a database — and turns it into business insights.

> **Skills demonstrated:** data cleaning · multi-table joins (ETL) · feature engineering · SQL / SQLite · exploratory data analysis · data visualization · reproducible project structure

---

## 📊 The business problem

Acting as a junior analyst at Olist (a Brazilian online marketplace), this project answers:

1. Is the business growing over time?
2. Which states drive the most revenue?
3. Do late deliveries hurt customer review scores?
4. Which product categories perform best?
5. How do customers prefer to pay?

## 🔑 Key findings

> _Replace these with your own results once you run the analysis._

- **Revenue grew steadily** across the dataset window, with a spike around the November shopping season.
- **São Paulo (SP) dominates** revenue, pointing to expansion opportunity in other states.
- **Late deliveries score dramatically lower** on reviews — delivery reliability is the clearest lever for satisfaction.
- **Credit card and boleto** are the leading payment methods.

## 📈 Selected visualizations

> _After running the notebooks, your charts are saved to `reports/figures/`. Embed them like this:_

![Monthly Revenue](reports/figures/monthly_revenue.png)
![Late vs. Reviews](reports/figures/late_vs_reviews.png)

---

## 🗂️ Project structure

```
brazilian-ecommerce-analysis/
├── README.md               ← you are here
├── PROJECT_GUIDE.md        ← full step-by-step build guide
├── requirements.txt        ← pip dependencies
├── environment.yml         ← conda environment
├── .gitignore
├── data/
│   ├── raw/                ← original Kaggle files (not committed)
│   └── processed/          ← cleaned, engineered outputs
├── notebooks/
│   ├── 01_understanding.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_engineering.ipynb
│   └── 04_analysis.ipynb
├── src/
│   └── pipeline.py         ← reusable ETL script
└── reports/
    └── figures/            ← saved charts
```

---

## 🚀 How to reproduce

1. **Clone and enter the repo**
   ```bash
   git clone https://github.com/YOUR_USERNAME/brazilian-ecommerce-analysis.git
   cd brazilian-ecommerce-analysis
   ```

2. **Create the environment**
   ```bash
   conda env create -f environment.yml
   conda activate ecommerce
   ```

3. **Download the data** (≈ 9 CSV files) into `data/raw/`
   ```bash
   kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw --unzip
   ```
   _(or download manually from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce))_

4. **Run the notebooks in order** (`01` → `04`), or build the clean dataset in one shot:
   ```bash
   python src/pipeline.py
   ```

---

## 🛠️ Tech stack

`Python` · `pandas` · `NumPy` · `matplotlib` · `seaborn` · `SQLite` · `Jupyter`

## 📚 Data source

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — ~100k orders from 2016–2018, released under a public license on Kaggle.

---

_Built as a learning project. See `PROJECT_GUIDE.md` for the full annotated walkthrough._
