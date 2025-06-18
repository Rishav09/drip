# DRIP: Data Retrieval • Ingest • Production

> Turn data drips into production ML streams.

**DRIP** is an end-to-end MLOps template/project that pulls live data from a API, enriches it, and ships models to production using k8 clusters. The idea to simulate an end-to-end MLOps production environment.

## Architecture
1. **Data Retrieval** – connectors for REST, WebSocket, or file drops  
2. **Ingest** – Kafka → object storage → DeltaLake  
3. **Transform** – Spark/DBT jobs, feature store sync  
4. **Modeling** – automated training & MLflow tracking  
5. **Production** – Dockerized FastAPI or Vertex AI endpoints  


