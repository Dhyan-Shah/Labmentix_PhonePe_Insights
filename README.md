# 💜 PhonePe Transaction Insights

> **End-to-end Data Science project** analyzing India's digital payments landscape using the PhonePe Pulse open-source dataset.  
> Built as part of the **Labmentix Data Science with AI/ML (6 Months Remote) Internship**.

---

## 📌 Project Overview

PhonePe Pulse is one of India's largest open-source datasets covering digital payment transactions across all states, districts, and pin codes from **2018 to 2024**. This project builds a complete data pipeline — from raw JSON extraction to an interactive Streamlit dashboard — to uncover strategic business insights.

### 🎯 Key Objectives
- Build an **ETL pipeline** to extract nested JSON data and load it into PostgreSQL
- Perform **Exploratory Data Analysis (EDA)** across 5 business case studies
- Create **15+ interactive visualizations** following the UBM framework
- Conduct **hypothesis testing** with 3 statistical tests
- Build and evaluate **3 ML models** for transaction amount prediction
- Deliver an **interactive Streamlit dashboard** for real-time data exploration

---

## 📊 Dataset

| Detail | Info |
|---|---|
| **Source** | PhonePe Pulse — Official Open Source Dataset |
| **GitHub Link** | 🔗 [https://github.com/PhonePe/pulse](https://github.com/PhonePe/pulse) |
| **Data Format** | Nested JSON files |
| **Time Period** | 2018 — 2024 |
| **Geographic Coverage** | 36 States & Union Territories |
| **Categories** | Transactions, Users, Insurance |
| **Granularity** | State → District → Pin Code |

### Clone the dataset
```bash
git clone https://github.com/PhonePe/pulse.git
```

---

## 🗂️ Project Structure

```
phonepe-transaction-insights/
│
├── 📁 notebooks/
│   ├── PhonePe_ETL.ipynb                        # ETL pipeline — JSON → PostgreSQL
│   ├── Convert_to_csv.ipynb                     # Export PostgreSQL tables to CSV
│   ├── PhonePe_Transaction_Insights.ipynb       # Main analysis notebook (local)
│   └── PhonePe_Transaction_Insights_Collab.ipynb # Google Colab version
│
├── 📁 Reference/
│   ├── Business Case Study.pdf                  # Project case study document
│   ├── Phone Pe.docx                            # Project requirements
│   ├── Phone Pe.pptx                            # Presentation
│   ├── Sample_EDA_Submission_Template.ipynb     # EDA template
│   └── Sample_ML_Submission_Template-2.ipynb   # ML template
│
├── 📄 app.py                                    # Streamlit dashboard
├── 📄 .gitignore
└── 📄 README.md
```

---

## 🗄️ Database Schema

9 PostgreSQL tables across 3 categories:

| Category | Tables |
|---|---|
| **Aggregated** | `aggregated_transaction`, `aggregated_user`, `aggregated_insurance` |
| **Map** | `map_transaction`, `map_user`, `map_insurance` |
| **Top** | `top_transaction`, `top_user`, `top_insurance` |

| Table | Rows |
|---|---|
| aggregated_transaction | 5,034 |
| aggregated_user | 6,732 |
| aggregated_insurance | 682 |
| map_transaction | 20,604 |
| map_user | 20,608 |
| map_insurance | 13,876 |
| top_transaction | 18,295 |
| top_user | 8,296 |
| top_insurance | 12,276 |

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.11 |
| **Database** | PostgreSQL 16 |
| **ETL** | pandas, SQLAlchemy, psycopg2, json, os |
| **Analysis** | pandas, numpy, scipy |
| **Visualization** | Plotly, Seaborn, Matplotlib |
| **ML Models** | scikit-learn (Linear Regression, Random Forest, Gradient Boosting) |
| **Dashboard** | Streamlit |
| **Version Control** | Git & GitHub |
| **Notebook** | Jupyter Notebook / Google Colab |

---

## 📋 Business Case Studies

5 case studies were selected from 9 available scenarios:

| # | Case Study | Key Question |
|---|---|---|
| 1 | 🏦 Decoding Transaction Dynamics | Which states and types drive growth? |
| 2 | 📱 Device Dominance & User Engagement | Which devices dominate? Where are dormant users? |
| 3 | 🛡️ Insurance Penetration & Growth | How is insurance adoption growing? |
| 4 | 🗺️ Transaction Analysis for Market Expansion | Where should PhonePe expand next? |
| 5 | 👥 User Registration Analysis | Where are registration-to-activation gaps? |

---

## 📈 Key Insights

- **Maharashtra, Karnataka & Telangana** drive 60%+ of total transaction value
- **Merchant payments** are the fastest growing category — overtaking P2P in recent years
- **Q4 (Oct–Dec)** is consistently the peak season across all states (festive effect)
- **Xiaomi** dominates PhonePe's device base with 30%+ user share
- **Insurance penetration is <1%** in every state — a massive untapped opportunity
- **Exponential insurance growth** since 2022, coinciding with IRDAI's national push
- **Registration-to-activation gap** is widening — millions of dormant registered users
- Top **pin codes are concentrated in Bengaluru, Mumbai, Hyderabad** tech corridors

---

## 🤖 ML Models

| Model | R² Score | RMSE |
|---|---|---|
| Linear Regression | baseline | — |
| Random Forest (GridSearchCV) | improved | — |
| **Gradient Boosting (RandomizedSearchCV)** | **best** | **lowest** |

**Target variable:** `log(transaction_amount)`  
**Features:** year, quarter (sin/cos), state_encoded, transaction_type_encoded, log(transaction_count)

---

## 🚀 How to Run Locally

### Prerequisites
```bash
pip install streamlit plotly pandas sqlalchemy psycopg2-binary requests numpy scikit-learn scipy seaborn matplotlib
```

### Step 1 — Clone the PhonePe dataset
```bash
git clone https://github.com/PhonePe/pulse.git
```

### Step 2 — Set up PostgreSQL
- Create a database called `phonepe_db`
- Run the ETL notebook: `notebooks/PhonePe_ETL.ipynb`
- Update your password in the connection string

### Step 3 — Run the Streamlit dashboard
```bash
streamlit run app.py
```
Opens at: `http://localhost:8501`

---

## ☁️ Run on Google Colab

1. Run `notebooks/Convert_to_csv.ipynb` locally to export all 9 tables as CSV
2. Upload the `phonepe_csv_data/` folder to Google Drive
3. Open `notebooks/PhonePe_Transaction_Insights_Collab.ipynb` in Colab
4. Mount Google Drive when prompted
5. Run all cells

---

## 🔐 Security Note

Sensitive credentials (PostgreSQL password) are **not** stored in this repository.  
Before running, update the DB connection string in each notebook and `app.py`:

```python
DB_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/phonepe_db"
```

For best practice, use a `.env` file:
```bash
pip install python-dotenv
```
```python
from dotenv import load_dotenv
import os
load_dotenv()
DB_URL = f"postgresql://postgres:{os.getenv('DB_PASSWORD')}@localhost:5432/phonepe_db"
```

---

## 📊 Dashboard Features

| Tab | Content |
|---|---|
| 🏠 Overview | KPI metrics, transaction trend, YoY growth chart |
| 💳 Transactions | Top states, districts, pincodes, quarterly seasonality |
| 👥 Users & Devices | Device brands, engagement scatter, registration trend |
| 🛡️ Insurance | Growth chart, gap analysis, treemap, penetration table |
| 🗺️ Geographic Map | India choropleth map with 4 selectable metrics |
| 📈 Business Insights | All 5 case studies with findings & recommendations |

All tabs have **sidebar filters** for Year, Quarter, State, and Transaction Type.

---

## 📁 Important Notes

- The `data/pulse/` folder is excluded from this repo via `.gitignore`
- Clone it separately from the [official PhonePe Pulse repo](https://github.com/PhonePe/pulse)
- The `.venv/` virtual environment folder is also excluded

---

## 👤 Author

**Dhyan Shah**  
Data Science Intern — Labmentix (AI/ML, 6 Months Remote)  

---

## 📄 License

This project uses the PhonePe Pulse dataset which is licensed under  
**[Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)**.

---

<div align="center">
  <b>💜 Built with Streamlit + PostgreSQL + Plotly</b><br>
  <i>PhonePe Pulse | 2018–2024 | Labmentix Data Science Internship</i>
</div>
