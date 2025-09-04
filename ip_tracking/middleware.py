from .models import RequestLog
from ipware import get_client_ip


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

        # We only log requests if we successfully found an IP address.
        if client_ip:
            RequestLog.objects.create(
                ip_address=client_ip,
                path=request.path
            )

        # Process the request and get the response to return to the user.
        response = self.get_response(request)

        return response