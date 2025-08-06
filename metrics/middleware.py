import time
from prometheus_client import Counter, Histogram
from django.urls import resolve

# Define Prometheus metrics
REQUEST_TIME_SECONDS = Histogram(
    "django_request_latency_seconds", "Request latency in seconds", ["method", "view"]
)
REQUESTS_TOTAL = Counter(
    "django_requests_total",
    "Total count of requests",
    ["method", "view", "status_code"],
)


class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.monotonic()

        try:
            view_name = resolve(request.path_info).view_name or "not_found"
        except Exception:
            view_name = "not_found"

        response = self.get_response(request)

        duration = time.monotonic() - start_time

        REQUEST_TIME_SECONDS.labels(method=request.method, view=view_name).observe(
            duration
        )

        REQUESTS_TOTAL.labels(
            method=request.method, view=view_name, status_code=response.status_code
        ).inc()

        return response
