from django.urls import path
from .views import metrics_view

app_name = 'metrics'

urlpatterns = [
    path('metrics/', metrics_view, name='metrics'),
]