# ip_tracking/views.py
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit


@ratelimit(
    key='ip',
    # Dynamically set the rate: 10/m for logged-in users, 5/m for anonymous
    rate=lambda request: '10/m' if request.user.is_authenticated else '5/m',
    method='POST',
    block=True
)
def sensitive_login_view(request):
    """
    A dummy view to simulate a login endpoint protected by rate limiting.
    """
    if request.method == 'POST':

        return HttpResponse("Login attempt processed successfully.")


    return HttpResponse("<h1>Login Page</h1><p>Submit your credentials via POST.</p>")