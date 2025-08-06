FROM python:3.13.5-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set the directory for multi-process Prometheus metrics
ENV PROMETHEUS_MULTIPROC_DIR /app/metrics-data

WORKDIR /app

# Install dependencies
COPY pyproject.toml /app/
RUN pip install --no-cache-dir .

# Copy the Django project code into the container
COPY . /app/

# Create the metrics directory within the container
RUN mkdir -p /app/metrics-data && chmod 777 /app/metrics-data

# Expose the port the app runs on
EXPOSE 8000

# Run the application using Gunicorn with multiple workers
# This demonstrates the multi-process metrics collection
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "core.wsgi:application"]