from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ModerationReport(models.Model):
    """Model for moderation reports."""
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        REVIEWING = 'reviewing', _('Reviewing')
        RESOLVED = 'resolved', _('Resolved')
        DISMISSED = 'dismissed', _('Dismissed')
    
    class ContentType(models.TextChoices):
        REVIEW = 'review', _('Review')
        DISCUSSION = 'discussion', _('Discussion')
        COMMENT = 'comment', _('Comment')
        BOOK = 'book', _('Book')
        USER = 'user', _('User')
    
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_made'
    )
    content_type = models.CharField(max_length=20, choices=ContentType.choices)
    content_id = models.IntegerField()
    reason = models.CharField(max_length=50, choices=[
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('inappropriate', 'Inappropriate Content'),
        ('copyright', 'Copyright Infringement'),
        ('fake', 'Fake/Impersonation'),
        ('other', 'Other'),
    ])
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_resolved'
    )
    resolution = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Moderation Report')
        verbose_name_plural = _('Moderation Reports')


class ModerationAction(models.Model):
    """Model for moderation actions taken."""
    
    class ActionType(models.TextChoices):
        WARNING = 'warning', _('Warning')
        SUSPENSION = 'suspension', _('Suspension')
        BAN = 'ban', _('Ban')
        CONTENT_REMOVED = 'content_removed', _('Content Removed')
        CONTENT_HIDDEN = 'content_hidden', _('Content Hidden')
    
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='moderation_actions'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='moderation_actions_received'
    )
    action_type = models.CharField(max_length=20, choices=ActionType.choices)
    reason = models.TextField()
    duration = models.DurationField(null=True, blank=True)  # For suspensions
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Moderation Action')
        verbose_name_plural = _('Moderation Actions')


class ContentFlag(models.Model):
    """Model for auto-detected content flags."""
    content_type = models.CharField(max_length=20, choices=ModerationReport.ContentType.choices)
    content_id = models.IntegerField()
    flag_type = models.CharField(max_length=50)
    confidence = models.DecimalField(max_digits=5, decimal_places=2)
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Content Flag')
        verbose_name_plural = _('Content Flags')
