from django.db import models
from django.conf import settings


class BookView(models.Model):
    """Track book views."""
    book_id = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class PageView(models.Model):
    """Track page views."""
    path = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class DailyAnalytics(models.Model):
    """Daily aggregated analytics."""
    date = models.DateField()
    total_views = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_royalties = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    new_users = models.PositiveIntegerField(default=0)
    new_books = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['date']


class UserAnalytics(models.Model):
    """User-level analytics."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    total_books_read = models.PositiveIntegerField(default=0)
    total_pages_read = models.PositiveIntegerField(default=0)
    total_time_spent = models.DurationField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    books_purchased = models.PositiveIntegerField(default=0)
    books_reviewed = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'User analytics'
