from django.db import models


class RequestLog(models.Model):
    ip_address = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=2000)

    class Meta:
        indexes = [models.Index(fields=['timestamp'])]
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"



