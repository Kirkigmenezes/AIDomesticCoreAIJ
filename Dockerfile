# Docker configuration for development
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY requirements-dev.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# Copy project
COPY . .

# Install package in development mode
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 aidev && \
    chown -R aidev:aidev /app

USER aidev

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Expose ports
EXPOSE 8000 8501 6006

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import aiplatform; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "pytest", "tests/"]
