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

![Architecture Diagram](https://github.com/user-attachments/assets/7e858dcd-a503-40a1-b53e-f514da25724b)

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

### Prerequisites:
- Docker & Docker Compose
- Python 3.10.8 (+ `requirements.txt`)
- AWS credentials with S3/Glue/Redshift access

## 🚀 Steps to Run the Project

1. **Clone the repository**
     ```bash
     git clone https://github.com/jenifa123/Smart-City-Realtime-Streaming-DE.git
     cd Smart-City-Realtime-Streaming-DE
     pip install -r requirements.txt

2. **Start Kafka and Spark using Docker Compose**
   - docker-compose up -d

3. **Run the Data Generator**
   - Execute the **`main.py`** script from PyCharm (or terminal).  
   - This script simulates **real-time smart city data** and pushes it to **Kafka topics**.  
   ```bash
   python main.py

 4. **Submit the Spark Job**
    ``` bash
    docker exec -it **spark-container-name** spark-submit \
      --master spark://spark-master:7077 \
      --conf spark.jars.ivy=/tmp/.ivy2 \
      --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk:1.11.469 \
      jobs/smart-city.py
    ```

5. **Data Flows to S3 bucket**
  -  Processed data is stored in your Amazon S3 bucket.
  -  Verify the data in the S3 console:
    <img width="1352" height="484" alt="image" src="https://github.com/user-attachments/assets/aee059ed-0ef7-4ab1-a2d7-f39ab912a5aa" />    


6. **AWS Glue (Data Catalog)**
  - Create a **Glue Crawler** to scan the S3 bucket.
    <img width="1190" height="507" alt="image" src="https://github.com/user-attachments/assets/2cef5bbe-06f3-4272-81b0-5386ed28326c" />

  - This will automatically create tables inside your **Glue Database** named as **smart_city_db**.
    <img width="1096" height="130" alt="image" src="https://github.com/user-attachments/assets/bf369b54-9f2d-429d-a8f5-bb71ba34c423" />

  - Once the crawler runs, you can verify the data by running a query in **Athena** or any query engine connected to Glue:
    <img width="1124" height="570" alt="image" src="https://github.com/user-attachments/assets/25bdb24b-1785-4c04-b94b-ee26bd8feeba" />

7. **Set Up Amazon Redshift**
   - Go to the **AWS Console → Redshift → Clusters**.  
   - Click **Create cluster** and configure:  
     - **Node type**: dc2.large (for testing) or ra3 (for production).  
     - **Cluster identifier**: smart-city-cluster  
     - **Database name**: smart_city_db  
     - **Master username & password**: set credentials you’ll remember.
     - **Attach an IAM Role** : RedshiftRole 
   - Wait for the cluster to be **available**.
   - Make sure the IAM Role has AmazonS3ReadOnlyAccess + AWSGlueConsoleFullAccess  
   - Update the **VPC Security Group** to allow access from your IP (or VPC where Glue/Athena runs).

    <img width="553" height="248" alt="image" src="https://github.com/user-attachments/assets/6d9b055b-d15d-442b-ac49-6c602322faf5" />

    <img width="1268" height="617" alt="image" src="https://github.com/user-attachments/assets/32e9bbca-a56a-4fb8-accb-42a198c1fa16" />


8. **Create an External Schema in Redshift (Spectrum)**
   - Connect to Redshift using the **Query Editor v2** (AWS Console) or any SQL client.  
   - Create an external schema that points to the Glue Catalog database:  
     ```sql
     CREATE EXTERNAL SCHEMA dev_smartcity
     FROM data catalog
     DATABASE 'smart_city_db'
     IAM_ROLE 'arn:aws:iam::123456789012:role/MyRedshiftRole'
     REGION 'ap-south-1';
     ```
     
9. **Query Data Stored in S3 via Redshift**
   - You can now directly query Glue tables (backed by S3 data):  
     ```sql
     SELECT * FROM dev_smartcity.emergency_data;
     ```
     <img width="553" height="176" alt="image" src="https://github.com/user-attachments/assets/2bf3215f-98a4-47f8-a290-5ab18a9fbc74" />

10. **Verify External Tables**
   - To check all tables available in your external schema:  
     ```sql
     SELECT * FROM svv_external_tables WHERE schemaname = 'dev_smartcity';
     ```
     <img width="553" height="141" alt="image" src="https://github.com/user-attachments/assets/cf09ae09-bd9b-41c6-bef3-4308c55e0823" />

## ✅ Conclusion  

This project showcases an end-to-end **Smart City Real-Time Data Pipeline** leveraging **Docker, Kafka, Spark, AWS S3, Glue, Athena, and Redshift**.  

Real-time events are ingested into **Kafka**, processed with **Spark Streaming**, and stored in **Amazon S3**. The data is then cataloged through **AWS Glue**, enabling seamless queries in **Athena**, while **Amazon Redshift** extends analytics capabilities by integrating external S3 data with internal Redshift datasets.  

By combining scalable open-source technologies with managed AWS services, the pipeline ensures **real-time processing, cost efficiency, and high availability**. This architecture provides a practical foundation for **Smart City analytics**, supporting use cases such as traffic monitoring, emergency response optimization, and environmental data insights. 


✨ Potential Enhancements:  
- Integrate **real-time dashboards** with Amazon QuickSight or Grafana.  
- Implement **automated alerts** using AWS Lambda and SNS.  
- Expand data sources to include **IoT devices and APIs**.  

