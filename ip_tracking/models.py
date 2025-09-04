from django.db import models


class RequestLog(models.Model):
    ip_address = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=2000)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    class Meta:
        indexes = [models.Index(fields=['timestamp'])]
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"

class BlockedIP(models.Model):
    ip_address = models.CharField(max_length=45, unique=True)

    class Meta:
        indexes = [models.Index(fields=['ip_address'])]
        verbose_name = "Blocked IP"
        verbose_name_plural = "Blocked IPs"

    def __str__(self):
        return self.ip_address

class SuspiciousIP(models.Model):
    ip_address = models.CharField(max_length=45, unique=True)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['ip_address'])]
        verbose_name = "Suspicious IP"
        verbose_name_plural = "Suspicious IPs"

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"