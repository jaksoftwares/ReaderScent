from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Discussion(models.Model):
    """Forum discussion model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='discussions'
    )
    book_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']
        verbose_name = _('Discussion')
        verbose_name_plural = _('Discussions')


class Post(models.Model):
    """Discussion post/reply model."""
    discussion = models.ForeignKey(
        Discussion,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class Follow(models.Model):
    """User follow model."""
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['follower', 'following']
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')


class Activity(models.Model):
    """User activity feed model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    activity_type = models.CharField(max_length=50)
    book_id = models.IntegerField(null=True, blank=True)
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
