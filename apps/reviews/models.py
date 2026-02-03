from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    """Book review model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    book_id = models.IntegerField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_spoiler = models.BooleanField(default=False)
    is_verified_purchase = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)
    helpful_votes = models.JSONField(default=list)  # List of user IDs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'book_id']
        ordering = ['-created_at']
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
    
    def __str__(self):
        return f"Review by {self.user.email} - Book {self.book_id}"


class Comment(models.Model):
    """Review comment model."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='review_comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
    
    def __str__(self):
        return f"Comment by {self.user.email} on Review {self.review.id}"


class Rating(models.Model):
    """User rating for books (simpler than full review)."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    book_id = models.IntegerField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'book_id']
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')
