import json
import time

from django.core.cache import cache
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class RateLimitMiddleware(MiddlewareMixin):
    """
    A custom Django middleware that limits requests from the same IP address
    to 10 per hour.

    This middleware uses a cache (e.g., Redis, LocMemCache) to track request
    timestamps for each IP. If an IP has sent 10 requests within the last hour,
    further requests get an HTTP 429 (Too Many Requests).

    How it works:
      1. Retrieve the client IP from request.META["REMOTE_ADDR"].
      2. Look up a cache key "rate_limit:<ip>" to see timestamps of recent requests.
      3. Filter out timestamps older than 1 hour.
      4. If the filtered list already has 10 entries, return HTTP 429.
      5. Otherwise, add the new timestamp and store it back in the cache with a 1-hour TTL.
    """

    def process_request(self, request):
        ip_address = request.META.get("REMOTE_ADDR")
        if ip_address:
            key = f"rate_limit:{ip_address}"
            # rate_limit_XXX: {}
            rate_limit = cache.get(key)
            if (
                rate_limit is not None
            ):  # even if there's an object but doesn't have a valid ip address if i didn't have None it will fail and still go through
                timestamps = json.loads(rate_limit)
            else:
                timestamps = []

            now = time.time()
            one_hour_ago = now - 3600
            updated_timestamps = [ts for ts in timestamps if ts > one_hour_ago]

            if len(updated_timestamps) >= 10:
                return HttpResponse("Rate limit exceeded, Max 10/H.", status=429)

            updated_timestamps.append(now)
            cache.set(key, json.dumps(updated_timestamps), 3600)

        return None
