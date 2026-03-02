# For Cloud Run CPU: use python:3.11-slim and install torch (CPU) in requirements.
# For Cloud Run with GPU: keep this base and ensure your Cloud Run service has GPU allocated.
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

RUN apt-get update && apt-get install -y --no-install-recommends python3-pip python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run sets PORT (default 8080). Container must listen on this port.
ENV PORT=8080
EXPOSE 8080
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]