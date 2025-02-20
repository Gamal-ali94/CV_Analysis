import json
import time

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class RateLimitMiddleware(MiddlewareMixin):
    """
    A custom Django middleware that limits requests from the same IP address
    based on configured settings.

    This middleware uses a cache (e.g., Redis, LocMemCache) to track request
    timestamps for each IP. If an IP has sent too many requests within the window,
    further requests get an HTTP 429 (Too Many Requests).

    Settings:
      - RATE_LIMIT_PER_MINUTE: Maximum number of requests per minute (default: 10)
      - RATE_LIMIT_WINDOW_SECONDS: Time window in seconds (default: 60)
    """

    def process_request(self, request):
        ip_address = request.META.get("REMOTE_ADDR")
        if ip_address:
            key = f"rate_limit:{ip_address}"
            rate_limit = cache.get(key)
            if rate_limit is not None:
                timestamps = json.loads(rate_limit)
            else:
                timestamps = []

            now = time.time()
            window_start = now - settings.RATE_LIMIT_WINDOW_SECONDS
            updated_timestamps = [ts for ts in timestamps if ts > window_start]

            if len(updated_timestamps) >= settings.RATE_LIMIT_PER_MINUTE:
                return HttpResponse(
                    f"Rate limit exceeded. Max {settings.RATE_LIMIT_PER_MINUTE} requests per {settings.RATE_LIMIT_WINDOW_SECONDS} seconds.",
                    status=429,
                )

            updated_timestamps.append(now)
            cache.set(
                key, json.dumps(updated_timestamps), settings.RATE_LIMIT_WINDOW_SECONDS
            )

        return None
