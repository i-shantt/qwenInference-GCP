# Qwen Inference on Google Cloud

This repository contains a containerized AI inference engine and web interface for the **Qwen** model. 

Built with **FastAPI**, this project serves both the backend inference API and a simple frontend UI from a single application. It is designed to be packaged with Docker and deployed to **Google Cloud Run** using hardware-accelerated instances.

### Tech Stack
* **Model:** Qwen (via Hugging Face `transformers`)
* **Framework:** FastAPI (Backend API & Frontend UI)
* **Containerization:** Docker
* **Deployment:** Google Cloud Run

### ⚠️ Important Cloud Run Hardware Requirements
When deploying this container to Google Cloud Run with GPU support, ensure your instance meets the required CPU-to-GPU ratio. To utilize **1 GPU (e.g., NVIDIA L4)**, Google Cloud requires a minimum allocation of **4 vCPUs**. Failing to allocate sufficient CPUs will result in deployment errors. 

*Note: Monitor your GCP billing dashboard closely, as GPU instances incur higher costs compared to standard CPU deployments.*

---

## Deployment Guide

Follow these steps to build and deploy the application to Google Cloud.

### 1. Build the Docker Image
Build the container image for your project:

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/SERVICE_NAME:v1 --project PROJECT_ID
```
### 2. Deploy using Google Cloud Run
```bash
gcloud run deploy qwen-inference \
  --image gcr.io/qweninference/qwen-inference:v1 \
  --platform managed \
  --region us-east4 \
  --project qweninference \
  --memory 16Gi \
  --cpu 4 \
  --gpu 1 \
  --gpu-type nvidia-l4 \
  --allow-unauthenticated
```
NOTE: To see and access the web application, make sure to add "/ui" at the end of the URL generated.
