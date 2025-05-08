from django.db import models
from django.contrib.auth.models import User


class SearchQuery(models.Model):
    """Model to log search queries for analytics."""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    query = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Search queries'
        ordering = ['-created_at']

    def __str__(self):
        return self.query
