# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (good for pdfminer, google libs, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port 8080 (Cloud Run expects this)
ENV PORT 8080

# Start Flask app with gunicorn (recommended for production)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
