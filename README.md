# 🚦 Smart City End-to-End Realtime Streaming Data Engineering Project

_A real-time data pipeline for smart cities powered by Kafka, Spark, Docker, and AWS._


## 📖 Project Overview

This project implements an **end-to-end real-time data streaming pipeline** designed for a **Smart City initiative**.  
It simulates and processes live data from a vehicle journey between **London and Birmingham**, capturing:

- 🚗 **Vehicle telemetry** (speed, fuel, performance)  
- 📍 **GPS location data**  
- 🚨 **Emergency incident alerts**  
- 🌦 **Weather conditions**  
- 📸 **Camera footage metadata**

  
## 🛠 Tech Stack

- **Stream Ingestion**: Apache Kafka (Dockerized, orchestrated using `docker-compose.yml`)
- **Stream Processing**: Apache Spark (Python-based structured streaming)
- **Storage**: S3 (parquet data), AWS Glue data catalog, Athena querying, Redshift data warehousing
- **Infrastructure**: Docker, IAM
---

##  Architecture

![Architecture Diagram](<img width="2880" height="1800" alt="architecture_smart_city" src="https://github.com/user-attachments/assets/30969d61-3524-4838-8465-204775d564a7" />)

---

##  Project Workflow

1. **Data Ingestion**  
   Simulated IoT data (e.g., vehicle metrics, GPS, emergency alerts, weather). Sent to Kafka topics.

2. **Stream Processing**  
   Spark Structured Streaming reads from Kafka and writes cleansed data to S3 (with checkpointing enabled for reliability).

3. **Cataloging & Querying**  
   AWS Glue crawlers build the data catalog; Athena executes queries directly over S3.

4. **Warehousing**  
   Curated data is loaded into Redshift for BI.

---

##  Setup Guide

### Prereqs:
- Docker & Docker Compose
- Python 3.x (+ `requirements.txt`)
- AWS credentials with S3/Glue/Redshift access

### Steps:

```bash
git clone https://github.com/jenifa123/Smart-City-Realtime-Streaming-DE.git
cd SmartCityProject
docker-compose up -d
pip install -r requirements.txt
