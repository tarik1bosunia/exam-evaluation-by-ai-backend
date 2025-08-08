# Use Python 3.9 as base
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create working directories for source, static, media, logs
RUN mkdir -p /app /app/static /app/media /app/logs

WORKDIR /app

# Install Python dependencies first for better caching
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy project source code
COPY . /app/

# Create a non-root user for better security
# Create a non-root user and set permissions
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl --fail http://localhost:8000/health/ || exit 1

# Entrypoint and CMD are omitted for docker-compose usage
