# Use an official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set Flask environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run the Flask app with Gunicorn
CMD exec gunicorn --bind :$PORT signed_url_service:app
