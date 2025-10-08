# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir yt-dlp

# Copy application files
COPY scraper.py .

# Create data directory for CSV output
RUN mkdir -p /app/data

# Set the data directory as a volume for persistence
VOLUME ["/app/data"]

# Run the scraper
CMD ["python", "scraper.py"]
