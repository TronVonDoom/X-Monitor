FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY monitor.py .

# Create volume for persistent data
VOLUME /app/data

# Set environment variable for data file location
ENV LAST_TWEET_FILE=/app/data/last_tweet_id.txt

# Run the monitor
CMD ["python", "-u", "monitor.py"]
