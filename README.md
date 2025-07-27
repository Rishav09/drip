# DRIP: Data Retrieval • Ingest • Production

> Turn data drips into production ML streams.

**DRIP** is an end-to-end MLOps template/project that pulls live data from a API, enriches it, and ships models to production using k8 clusters. The idea to simulate an end-to-end MLOps production environment.

## Architecture
1. **Data Retrieval** – Ingesting realtime data from the Kraken websocket API, and historic data from the Rest API
2. **Ingest** – Using Kafka to store it. 
3. **Transform** – Using Quixstreams to operate it upon. 
4. **Modeling** – RisingWave is used on top of it, along with grafana for the visualisaiton part. 
5. **Production** – Dockerized FastAPI or Vertex AI endpoints  


