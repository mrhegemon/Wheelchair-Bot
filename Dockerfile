FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcamera-apps \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/ ./services/
COPY web_client/ ./web_client/
COPY config/ ./config/
COPY start.sh stop.sh ./

# Make scripts executable
RUN chmod +x start.sh stop.sh

# Expose ports
EXPOSE 8000 8001 8002 8003 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start services
CMD ["./start.sh"]
