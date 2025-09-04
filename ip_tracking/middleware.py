# ip_tracking/middleware.py
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django_ip_geolocation.backends import IPGeolocationAPI
from .models import RequestLog, BlockedIP
from ipware import get_client_ip
import logging

logger = logging.getLogger(__name__)


class IPLoggingMiddleware:
    """
    Custom middleware to log incoming requests to the database.

    This middleware captures the client's IP address, the requested path,
    and saves it to the RequestLog model for every incoming request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip, _ = get_client_ip(request)

        # Log requests only if an IP address is found
        if client_ip:
            if BlockedIP.objects.filter(ip_address=client_ip).exists():
                return HttpResponseForbidden(
                    "<h1>Forbidden</h1><p>Your IP address has been blocked.</p>"
                )

            # Check cache for geolocation data
            cache_key = f'ip_geo_{client_ip}'
            geo = cache.get(cache_key)

            if geo is None:
                try:
                    backend = IPGeolocationAPI()
                    backend.ip_address = client_ip
                    backend.geolocate()
                    backend._parse()

                    geo = {
                        'country': backend._country['name']
                        if hasattr(backend, '_country') and backend._country else '',
                        'city': backend._city if hasattr(backend, '_city') else '',
                    }

                    cache.set(cache_key, geo, 86400)  # Cache for 24 hours
                except Exception as e:
                    logger.error(f"Geolocation error: {e}")
                    geo = {'country': '', 'city': ''}

            # Log request to the database
            RequestLog.objects.create(
                ip_address=client_ip,
                path=request.path,
                country=geo['country'],
                city=geo['city']
            )


        response = self.get_response(request)
        return response
