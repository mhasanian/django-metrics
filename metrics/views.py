import os
import time
from django.http import HttpResponse
from prometheus_client import generate_latest, CollectorRegistry, multiprocess, REGISTRY
from django.conf import settings
from django.http import JsonResponse
from .database import redis_client

def prometheus_metrics_view(request):
    """
    Exposes Prometheus metrics.
    If the PROMETHEUS_MULTIPROC_DIR environment variable is set, it will aggregate
    metrics from all worker processes.
    """
    # TODO: make sure PROMETHEUS_MULTIPROC_DIR exists and is writable

    if "PROMETHEUS_MULTIPROC_DIR" in os.environ:
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
    else:
        # for single-process environments (like 'runserver') Use the default global registry
        registry = REGISTRY
    metrics_page = generate_latest(registry)
    return HttpResponse(
        metrics_page, content_type="text/plain; version=0.0.4; charset=utf-8"
    )

def redis_metrics_view(request):
    redis_key = getattr(settings, "METRICS_REDIS_KEY", "django:metrics:response_times")
    window_size = getattr(settings, "METRICS_WINDOW_SECONDS", 10)

    now = time.time()
    window_start = now - window_size

    # Clean up old entries first
    redis_client.zremrangebyscore(redis_key, 0, window_start)

    # Fetch current response times
    response_times = redis_client.zrangebyscore(redis_key, window_start, now, withscores=False)

    if not response_times:
        avg_time = 0.0
    else:
        times = list(map(float, response_times))
        avg_time = sum(times) / len(times)

    return JsonResponse({
        "avg_response_time_last_10s": round(avg_time, 6),
        "count": len(response_times),
    })