# Use an official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/app/model_cache
ENV HF_HOME=/app/model_cache
ENV HF_DATASETS_CACHE=/app/model_cache
ENV XDG_CACHE_HOME=/app/model_cache

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create cache directory and download model as root
RUN mkdir -p /app/model_cache && \
    python -c "from sentence_transformers import SentenceTransformer; \
    import os; \
    print('Cache directory:', os.environ.get('TRANSFORMERS_CACHE')); \
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', \
                               cache_folder='/app/model_cache'); \
    print('Model downloaded and cached')"

# Copy the rest of the application
COPY . .

# Copy the recipes.docx file into the container
COPY recipes.docx recipes.docx

# Copy book images
COPY static/ static/

# Create non-root user
RUN adduser -u 5678 --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

CMD ["python", "ui.py"]