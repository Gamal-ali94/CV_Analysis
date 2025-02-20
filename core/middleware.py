import time
import json

from django.core.cache import cache
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class RateLimitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        if ip_address:
            key = f"rate_limit:{ip_address}"
            #rate_limit_XXX: {}
            rate_limit = cache.get(key)
            if rate_limit is not None: #even if there's an object but doesn't have a valid ip address if i didn't have None it will fail and still go through
                timestamps = json.loads(rate_limit)
            else:
                timestamps = []
            
            now = time.time()
            one_hour_ago = now - 3600 
            updated_timestamps = [ts for ts in timestamps if ts > one_hour_ago]
            
            if len(updated_timestamps) >= 10:
                return HttpResponse("Rate limit exceeded", status=429)
            
            updated_timestamps.append(now)
            cache.set(key, json.dumps(updated_timestamps), 3600)
            
        return None