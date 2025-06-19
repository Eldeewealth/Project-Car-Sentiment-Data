# 🚗 Auto Intel Project

This project is a Scrapy-based web crawler designed to extract car reviews and automotive news from [AutoExpress UK](https://www.autoexpress.co.uk/). The scraped data is stored in a PostgreSQL database for analysis, reporting, or powering data-driven apps.

---

## 📌 Features

- Scrapes detailed car reviews (title, author, verdict, rating, etc.)
- Extracts latest car-related news articles
- Stores structured data into PostgreSQL
- Unified Scrapy pipeline with data validation
- Airflow integration for automated scheduling (WIP)

---

## 🛠️ Project Structure

auto_intel_project/
│
├── auto_intel/
│   ├── items.py              # Scrapy data models
│   ├── pipelines.py          # PostgreSQL pipeline (excluded from Git)
│   ├── models.py             # Pydantic models for validation
│   └── spiders/
│       ├── auto_reviews.py   # Scraper for car reviews
│       └── auto_news.py      # Scraper for car news
│
├── airflow_home/             # Airflow config and DAGs
├── venv/ or airflow_env/     # Python virtual environments
└── README.md
🧰 Setup Instructions
1. Clone the Repo

git clone https://github.com/Eldeewealth/Project-Test-Auto-Intel.git
cd Project-Test-Auto-Intel/auto_intel_project
2. Create Virtual Environment

python -m venv venv
venv\Scripts\activate  # Windows
3. Install Dependencies

pip install -r requirements.txt
4. Set up PostgreSQL
Create a PostgreSQL database and update your pipelines.py connection string accordingly.

🕷️ Running the Crawlers
Crawl Car Reviews

scrapy crawl auto_reviews
Crawl Auto News

scrapy crawl auto_news
⏱️ Automate with Airflow (Optional)
Activate your Airflow environment:

airflow_env\Scripts\activate
Set AIRFLOW_HOME and DB path:

set AIRFLOW_HOME=C:/your/project/path/airflow_home
set AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=sqlite:////C:/your/project/path/airflow_home/airflow.db
Initialize Airflow:

airflow db migrate
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password yourpassword
Run:

airflow webserver
airflow scheduler
🧾 License
MIT License © 2025 Eldeewealth
