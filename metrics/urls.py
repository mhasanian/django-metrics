from django.urls import path
from .views import prometheus_metrics_view, redis_metrics_view

app_name = 'metrics'

urlpatterns = [
    path('metrics/', prometheus_metrics_view, name='metrics'),
    path('redis-metrics/', redis_metrics_view, name='redis-metrics'),
]