# 🌦️ Weather Data Engineering Pipeline

An end-to-end Data Engineering project designed to ingest, transform, validate, and prepare weather data for analytics and visualization using Power BI.

## 🎯 Project Objectives

- Ingest weather data from a data source.
- Transform raw data into structured and analytics-ready datasets.
- Organize data processing into Bronze, Silver, and Gold layers.
- Implement data quality checks to improve reliability.
- Export processed data for Power BI reporting.

## 🏗️ Architecture

The pipeline follows a Medallion Architecture approach:

- **Bronze Layer:** Stores ingested raw weather data.
- **Silver Layer:** Cleans, standardizes, and transforms the data.
- **Gold Layer:** Produces curated datasets for reporting and analytics.

The processed data can then be exported for visualization in Power BI.

## 🛠️ Technologies

- **Language:** Python
- **Data Engineering:** ETL / ELT concepts, data transformation
- **Data Quality:** Validation and quality checks
- **Orchestration:** Python pipeline orchestration
- **Business Intelligence:** Power BI
- **Version Control:** Git and GitHub

## 📂 Project Structure

```text
weather-data-engineering-pipeline/
├── weather_ingestion.py
├── silver_transformation.py
├── gold_transformation.py
├── quality_checks.py
├── dag_pipeline.py
├── export_powerbi.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Pipeline Components

| File | Description |
|---|---|
| `weather_ingestion.py` | Ingests weather data from the configured source. |
| `silver_transformation.py` | Cleans and transforms ingested data. |
| `gold_transformation.py` | Prepares curated datasets for analytics. |
| `quality_checks.py` | Runs data quality validations. |
| `dag_pipeline.py` | Defines the pipeline execution workflow. |
| `export_powerbi.py` | Prepares or exports processed data for Power BI. |

## 🔄 Workflow

1. Ingest weather data.
2. Store or prepare the raw data.
3. Clean and transform data in the Silver layer.
4. Apply data quality checks.
5. Generate analytics-ready datasets in the Gold layer.
6. Export the processed data for Power BI.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/capriiisuun/weather-data-engineering-pipeline.git
cd weather-data-engineering-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

After creating `requirements.txt` with the libraries required by the project:

```bash
pip install -r requirements.txt
```

### 4. Run the pipeline

Check the configuration and execution order in `dag_pipeline.py`, then run the pipeline using the entry point defined in the code.

```bash
python dag_pipeline.py
```

**Note:** The actual data source, configuration, dependencies, and execution order must be configured according to the project implementation.

## 📊 Business Intelligence

Power BI can be used to visualize the processed weather data and build reports based on the Gold layer.

Screenshots of the dashboard can be added here.

## 🧪 Data Quality

The `quality_checks.py` module is intended to validate data quality. Checks may include missing values, duplicate records, data types, and consistency rules, depending on the implemented validations.

## 👩‍💻 Author

**Alaa Elkorchi**

AI & Data Science Engineering Student — EMSI

GitHub: [@capriiisuun](https://github.com/capriiisuun)

---

⭐ Feel free to explore this repository and its data engineering workflow.
