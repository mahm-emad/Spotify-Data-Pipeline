# 🎵 Spotify ETL Data Pipeline Project

This project implements an end-to-end **ETL pipeline** for analyzing Spotify track data using:

- **Apache Airflow** (ETL orchestration)
- **Apache Spark** (data transformation)
- **PostgreSQL** (as both staging area and data warehouse)
- **Docker Compose** (for containerized development)
- **Jupyter Notebook** (for exploration)

---

## 📊 Dataset

**Source**: [Spotify Dataset (1921–2020, 600K Tracks)](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks)

The dataset includes historical track-level metadata such as artist names, genres, popularity, release dates, and more.

---

## 🧱 Architecture Overview

![System_Architechture](https://github.com/mahm-emad/Spotify-Data-Pipeline/blob/main/Architecture.jpg)

- **Airflow** schedules and orchestrates the ETL process.
- **Spark** transforms data from staging and loads it into the DWH.
- **Docker** ensures a consistent and reproducible environment.

---

## 🐳 Dockerized Components

| Component           | Description                            | Port     |
|---------------------|----------------------------------------|----------|
| `Airflow Webserver` | DAG orchestration UI                   | `8090`   |
| `Postgres`          | Staging database (Staging DB)          | `5442`   |
| `Postgres_DW`       | Data warehouse                         | `5433`   |
| `Spark`             | Spark master container                 | `7077`   |
| `Jupyter`           | Pyspark exploration environment        | `8085`   |

---

## 📁 Folder Structure

```
.
├── dags/                  # Airflow DAGs
├── spark/
│   ├── app/               # Spark transformation scripts
│   └── resources/         # Input data / SQL
├── notebooks/             # Jupyter Notebooks for exploration
├── data/                  # Raw CSV files
├── JDBC_Driver/           # PostgreSQL JDBC driver for Spark
├── docker-compose.yml
├── Dockerfile             # Extends Airflow image with Java/Spark
```

---

## 🧪 DWH Overview

✅ The data warehouse is structured using a Snowflake Schema, which handles normalized relationships, including a bridge table (`dim_artist_genre`) for many-to-many mappings.

The data warehouse follows a Snowflake Schema design:

A central `track_fact` table captures track-level metrics, with track popularity as the primary measure. Additional fields include track duration and snapshot date.

Dimension tables provide context:

`dim_artists`: metadata about artists

`dim_tracks`: attributes of tracks such as title and release year

`dim_genres`: list of music genres

`dim_date`: calendar-related attributes for time-based analysis

A bridge table `dim_artist_genre` represents the many-to-many relationship between artists and genres.

The schema is fully normalized, making it efficient for complex analytical queries and reducing data redundancy.

![DWH_Schema](https://github.com/mahm-emad/Spotify-Data-Pipeline/blob/main/DWH%20Schema.png)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/spotify-etl-pipeline.git
cd spotify-etl-pipeline
```

### 2. Run with Docker Compose
```bash
docker-compose up --build
```

### 3. Access Services

- Airflow: [http://localhost:8090](http://localhost:8090)
- Jupyter Notebook: [http://localhost:8085](http://localhost:8085)
- PostgreSQL (Staging): `localhost:5442`
- PostgreSQL (DWH): `localhost:5433`

> Default Airflow credentials: `airflow / airflow`

---

## 🔄 ETL Process

1. **Extract**: CSV files are loaded into PostgreSQL (App DB)
2. **Transform**: Spark reads from staging, cleans, and aggregates data
3. **Load**: Processed data is written into the DWH (Postgres)

All steps are orchestrated by Apache Airflow DAGs.

---

## 📚 Tools & Technologies

- Apache Airflow 2.10.5
- Apache Spark 3.5.1
- PostgreSQL 13
- Docker & Docker Compose
- Jupyter (Pyspark Notebook)
- DBeaver (used for DB connections and ERD)

---

## 📌 Future Improvements

- Automate daily Spotify ingestion via API
- Visualize KPIs using Power BI or Grafana
