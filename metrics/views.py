import os
from django.http import HttpResponse
from prometheus_client import generate_latest, CollectorRegistry, multiprocess, REGISTRY


def metrics_view(request):
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
