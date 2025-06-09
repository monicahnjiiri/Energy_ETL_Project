# ⚡ Energy Insights ETL Project

An end-to-end pipeline that extracts, cleans, loads, automates, predicts, and visualizes Germany’s energy data.


## 📁 Project Folder Structure

<img width="209" alt="image" src="https://github.com/user-attachments/assets/a8f4985c-39c4-4136-b33f-311ff32bd19d" />


---

## 📌 Contents

1. [📊 Introduction](#introduction)
2. [🔍 Data Extraction](#data-extraction)
3. [🧹 Data Transformation](#data-transformation)
4. [🗃️ Data Loading](#data-loading)
5. [⏱️ Airflow Automation](#airflow-automation)
6. [🤖 Model, API, and Streamlit App](#model-api-and-streamlit)
7. [📈 Power BI Dashboard](#power-bi-dashboard)

---

## 📊 Introduction

This project aims to analyze and visualize Germany's energy load vs renewable generation. It automates ETL workflows, trains a predictive model, and hosts a dashboard to provide real-time insights.

---

## 🔍 Data Extraction

We start by extracting data from raw CSV files using `Extract.py`. The script focuses on German data only and ensures proper timestamp formatting.

---

## 🧹 Data Transformation

`Transform.py` handles missing values (without using zero-filling), filters only German TSO regions, and separates the dataset into:
- Forecasted Load
- Actual Load
- Actual Generation

The cleaned files are saved to `data/processed/`.

---

## 🗃️ Data Loading

`Load.py` loads the transformed data into a MySQL database using `pymysql` for secure connection. Large file handling and `.env` secrets are excluded via `.gitignore`.

---

## ⏱️ Airflow Automation

ETL tasks are orchestrated using Apache Airflow. The DAG (`dags/energy_etl_dag.py`) runs daily, and Docker Compose handles containerization for both MySQL and Airflow services. It also sends alert in case of failure.
<img width="278" alt="image" src="https://github.com/user-attachments/assets/a34845d9-81a1-4882-b138-340e4fe22719" />
<img width="234" alt="image" src="https://github.com/user-attachments/assets/82b9c4c0-d99d-40bc-9c06-c6a606f3ae7c" />



---

## 🤖 Model, API, and Streamlit

A regression model is trained using `model_training.py` based on:
- Time features
- Forecasted load

### ✅ FastAPI
The trained model is served via a FastAPI endpoint (`FastAPI.py`) for real-time prediction.
<img width="488" alt="image" src="https://github.com/user-attachments/assets/b35d31cd-526c-49d1-bf2f-71d3bdc7f600" />

### 💻 Streamlit
`Streamlit.py` allows users to input time + forecast values and receive predicted actual load instantly.
<img width="383" alt="image" src="https://github.com/user-attachments/assets/7bb7e6e2-49dc-4712-b12c-d2e9c612dbde" />

> **Note**: Model weights (`model.pkl`) are excluded from Git due to size.

---

## 📈 Power BI Dashboard

A Power BI dashboard was created to visualize:
- Forecast vs Actual Load (TSO-level)
- Renewable Generation Share
- Yearly Trends
- Portion of Demand Met by Renewables

<img width="452" alt="image" src="https://github.com/user-attachments/assets/b4aada7a-10c7-464e-8f66-677b05449571" />


🔗 [Click to view the live dashboard](https://app.powerbi.com/groups/me/reports/fd9860f2-002f-4210-b5d3-815142e3a8df/cc18c7829bb853baacf2?experience=power-bi)

---




