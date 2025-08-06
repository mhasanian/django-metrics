import time
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from ..database import redis_client

class RedisMetricsMiddleware(MiddlewareMixin):
    """
    Middleware to track response times and store in Redis sorted set.
    """

    REDIS_KEY = getattr(settings, "METRICS_REDIS_KEY", "django:metrics:response_times")
    WINDOW_SIZE_SECONDS = getattr(settings, "METRICS_WINDOW_SECONDS", 10)

    def process_request(self, request):
        # Start timer on request start
        request._start_time = time.monotonic()

    def process_response(self, request, response):
        # Calculate elapsed time
        start = getattr(request, "_start_time", None)
        if start is not None:
            elapsed = time.monotonic() - start
            timestamp = time.time()

            # Add response time to Redis sorted set with timestamp as score
            redis_client.zadd(self.REDIS_KEY, {elapsed: timestamp})

            # Remove old entries outside the rolling window
            min_score = 0
            max_score = timestamp - self.WINDOW_SIZE_SECONDS
            redis_client.zremrangebyscore(self.REDIS_KEY, min_score, max_score)

        return response