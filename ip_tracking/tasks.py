from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    now = timezone.now()
    last_hour = now - timedelta(hours=1)

    # Flag high request rates (>100 total requests/hour)
    high_req_ips = (
        RequestLog.objects.filter(timestamp__gte=last_hour)
        .values('ip_address')
        .annotate(count=Count('ip_address'))
        .filter(count__gt=100)
    )
    for entry in high_req_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            defaults={'reason': f"High request rate ({entry['count']} > 100/hour)"}
        )

    # Flag multiple accesses to sensitive paths (>5/hour)
    sensitive_paths = ['/admin', '/login']
    sensitive_access = (
        RequestLog.objects.filter(timestamp__gte=last_hour, path__in=sensitive_paths)
        .values('ip_address')
        .annotate(count=Count('ip_address'))
        .filter(count__gt=5)
    )
    for entry in sensitive_access:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            defaults={'reason': f"Multiple accesses to sensitive paths ({entry['count']} > 5/hour)"}
        )