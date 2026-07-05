# 📈 FinSight

> **An End-to-End Financial Analytics ETL Platform built using Python.**

FinSight is a modular data engineering project that automates the complete workflow of collecting historical stock market data, transforming it into analysis-ready datasets, storing it in a relational database, and generating analytical insights.

The project is designed to demonstrate **ETL architecture**, **software engineering practices**, and **modular Python development**, with a roadmap toward a production-ready financial analytics platform.

---

# 🚀 Project Overview

The current version of FinSight implements a complete **Batch ETL Pipeline**.

The workflow is:

```
Yahoo Finance API
        │
        ▼
Data Extraction
        │
        ▼
Data Cleaning & Feature Engineering
        │
        ▼
SQLite Database
        │
        ▼
Financial Analytics
        │
        ▼
Console Report + Logs
```

The project is intentionally built using a modular architecture so that every component can be extended independently.

---

# ✨ Current Features

### Data Extraction

- Downloads historical stock market data using Yahoo Finance
- Supports multiple stock tickers
- Saves raw data as CSV files
- Handles extraction failures gracefully

---

### Data Transformation

The transformation layer performs:

- Duplicate removal
- Missing value handling
- Column standardization
- Date formatting
- Chronological sorting

Feature Engineering:

- Daily Return
- Daily Percentage Return
- 7-Day Moving Average
- 30-Day Moving Average
- 30-Day Rolling Volatility

Processed datasets are saved separately from raw datasets.

---

### Database Layer

Processed data is automatically loaded into SQLite.

Features include:

- Automatic table creation
- Duplicate-safe inserts
- Structured schema
- Persistent storage

---

### Analytics

The analytics module computes:

- Highest Closing Price
- Lowest Closing Price
- Average Daily Return
- Highest Trading Volume
- Highest Volatility

A formatted report is generated after every pipeline execution.

---

### Logging

Centralized logging captures every pipeline stage:

- Extraction
- Transformation
- Database Loading
- Analytics
- Errors
- Warnings

Logs are written both to the console and to log files.

---

# 📂 Project Structure

```
fininsight/
│
├── config/
│   ├── settings.py
│   └── logging_config.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── db/
│
├── logs/
│
├── src/
│   ├── extraction/
│   ├── transformation/
│   ├── database/
│   ├── analytics/
│   └── pipeline/
│
├── tests/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🏗️ Project Architecture

```
main.py
      │
      ▼
Pipeline Runner
      │
      ▼
Extraction
      │
      ▼
Transformation
      │
      ▼
Database
      │
      ▼
Analytics
      │
      ▼
Report Generation
```

Each module has a single responsibility, making the project easier to maintain, test, and extend.

---

# ⚙️ Technologies Used

- Python
- Pandas
- NumPy
- SQLite
- yfinance
- Logging
- Git
- GitHub

---

# ▶️ Running the Project

## Clone Repository

```bash
git clone https://github.com/sarvesh0005/fininsight.git
cd fininsight
```

---

## Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Pipeline

```bash
python main.py
```

---

# 📊 Pipeline Output

Running the pipeline performs the following:

- Downloads one year of historical stock data
- Stores raw datasets
- Cleans and transforms data
- Engineers financial features
- Loads processed data into SQLite
- Computes analytical metrics
- Generates reports
- Creates execution logs

---

# 📁 Generated Files

After execution the project automatically creates:

```
data/raw/
```

Historical downloaded datasets

```
data/processed/
```

Cleaned and transformed datasets

```
data/db/finsight.db
```

SQLite database

```
logs/
```

Execution logs

---

# 🧠 Engineering Concepts Demonstrated

This project demonstrates:

- ETL Pipeline Design
- Data Engineering Workflow
- Modular Software Architecture
- Separation of Concerns
- Feature Engineering
- Configuration Management
- Centralized Logging
- Database Integration
- Error Handling
- Pipeline Orchestration

---

# 📌 Current Status

Current Version:

**MVP (Minimum Viable Product)**

The current implementation is a manually triggered **Batch ETL Pipeline**.

Execution is started by running:

```bash
python main.py
```

---

# 🚀 Future Roadmap

The long-term goal is to evolve FinSight into a production-ready financial analytics platform.

## Version 2

- PostgreSQL Integration
- FastAPI REST API
- Streamlit Dashboard
- Docker Containerization
- Configuration using Environment Variables
- Data Validation
- Better Exception Handling

---

## Version 3

- Automated Daily Pipeline Scheduling
- Apache Airflow / Prefect Orchestration
- Incremental Data Loading
- Data Quality Monitoring
- CI/CD with GitHub Actions

---

## Version 4

- Machine Learning Price Forecasting
- Financial Risk Analytics
- Portfolio Analytics
- Interactive Dashboard
- Cloud Deployment (AWS/GCP/Azure)

---

# 🎯 Why I Built This Project

The objective of FinSight is to strengthen practical skills in:

- Python Software Engineering
- Data Engineering
- ETL Pipeline Development
- Financial Data Processing
- Modular System Design

while building a project that closely resembles real-world production workflows.

---

# 👨‍💻 Author

**Sarvesh Maurya**

Machine Learning Engineer | Data Science | Operations Research

GitHub:

https://github.com/sarvesh0005

LinkedIn:

https://www.linkedin.com/in/sarvesh-maurya005

---

# ⭐ Project Status

**Actively Under Development**

This repository is continuously being improved with new features and production-grade engineering practices.
