# Django Metrics

A Django middleware for exporting Prometheus metrics, built to handle requests in multi-process environments like Gunicorn.
Built for interview code challenge!

## Installation

```bash
pip install django-metrics
```

## Setup

#### 1. Add to `INSTALLED_APPS`

In your project's `settings.py`, add `metrics` to your installed apps.

```python
# settings.py

INSTALLED_APPS = [
    # ... other apps
    'metrics',
]
```

#### 2. Add the Middleware

Add the middleware to your `settings.py`. It's best to place it near the top of the list to accurately measure total request time.

```python
# settings.py

MIDDLEWARE = [
    'metrics.middleware.PrometheusMetricsMiddleware',
    # ... other middleware
]
```

#### 3. Include the Metrics URL

In your project's main `urls.py`, include the metrics endpoint.

```python
# your_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # ... your other urls
    path('', include('metrics.urls')), # Includes the /metrics endpoint
]
```

## 🚀 Running in Production (Gunicorn)

To handle millions of requests, you'll likely use a WSGI server like Gunicorn with multiple workers. To ensure metrics from all workers are collected, you **must** set the `PROMETHEUS_MULTIPROC_DIR` environment variable.

1.  Create a directory that your application's user can write to.

    ```bash
    mkdir /tmp/prometheus_metrics
    ```

2.  Set the environment variable when running Gunicorn.

    ```bash
    export PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus_metrics
    # Clean the directory before starting
    rm -f /tmp/prometheus_metrics/*.db
    
    gunicorn your_project.wsgi -w 4 --bind 0.0.0.0:8000
    ```

Now, when you access `http://localhost:8000/metrics`, you will see the aggregated data from all 4 worker processes.