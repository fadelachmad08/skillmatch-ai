FROM python:3.11-slim

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create writable storage directory for HF Spaces (non-root user)
RUN mkdir -p /code/data/storage && chmod -R 777 /code/data

# Copy all application files
COPY . .

# HF Spaces uses port 7860 by default
ENV PORT=7860
EXPOSE 7860

# Start with gunicorn, 2 workers, 120s timeout for ML model loading
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "2", "--timeout", "120", "app:app"]
