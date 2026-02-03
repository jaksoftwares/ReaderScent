from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    """User notification model."""
    
    class Type(models.TextChoices):
        ORDER_CONFIRMATION = 'order_confirmation', _('Order Confirmation')
        ORDER_COMPLETED = 'order_completed', _('Order Completed')
        NEW_REVIEW = 'new_review', _('New Review')
        REVIEW_RESPONSE = 'review_response', _('Review Response')
        FOLLOW = 'follow', _('New Follower')
        BOOK_PUBLISHED = 'book_published', _('Book Published')
        PROMOTION = 'promotion', _('Promotion')
        SYSTEM = 'system', _('System')
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=50, choices=Type.choices)
    title = models.CharField(max_length=200)
    message = models.TextField()
    data = models.JSONField(default=dict)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
    
    def __str__(self):
        return f"{self.notification_type} - {self.user.email}"


class EmailTemplate(models.Model):
    """Email template model for notifications."""
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    html_body = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Email Template')
        verbose_name_plural = _('Email Templates')
    
    def __str__(self):
        return self.name


class PushSubscription(models.Model):
    """Push notification subscription model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='push_subscriptions'
    )
    endpoint = models.URLField(max_length=500)
    p256dh = models.CharField(max_length=100)
    auth = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'endpoint']
        verbose_name = _('Push Subscription')
        verbose_name_plural = _('Push Subscriptions')
