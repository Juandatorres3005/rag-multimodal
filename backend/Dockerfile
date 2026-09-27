FROM python:3.11-slim

WORKDIR /app

# Install build and runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmupdf-dev \
    && rm -rf /var/lib/apt-get/lists/*

# Copy requirements and install (layer caches on requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create data persistence directories
RUN mkdir -p chroma_db extracted_images

# Copy application code
COPY backend/ ./backend/

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/', timeout=5)" || exit 1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
