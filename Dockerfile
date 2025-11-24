# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install required Python packages
RUN pip install --no-cache-dir requests

# Copy the monitoring script
COPY x_monitor.py /app/
COPY config.env /app/

# Create directory for state file
RUN mkdir -p /app/data

# Run the script
CMD ["python", "-u", "x_monitor.py"]
