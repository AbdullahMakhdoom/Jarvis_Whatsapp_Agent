# Use an appropriate base image
FROM python:3.12-slim

# Install the project into `/app`
WORKDIR /app

# Set environment variables (e.g., set Python to run in unbuffered mode)
ENV PYTHONUNBUFFERED=1

# Install system dependencies for building libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first for better layer caching
COPY requirements.txt /app/

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/data

# Define volumes
VOLUME ["/app/data"]

# Expose the port
EXPOSE 8080

# Run the FastAPI app using uvicorn
CMD ["fastapi", "run", "interfaces/whatsapp/webhook_endpoint.py", "--port", "8080", "--host", "0.0.0.0"]
