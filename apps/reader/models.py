from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ReadingProgress(models.Model):
    """Track user's reading progress for each book."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reading_progress'
    )
    book_id = models.IntegerField()
    current_page = models.PositiveIntegerField(default=0)
    current_chapter = models.ForeignKey(
        'books.Chapter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reading_progress'
    )
    percent_complete = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    last_position = models.TextField(blank=True)  # JSON for detailed position
    last_read_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'book_id']
        verbose_name = _('Reading Progress')
        verbose_name_plural = _('Reading Progress')
    
    def __str__(self):
        return f"{self.user.email} - Book {self.book_id}"


class Highlight(models.Model):
    """User highlights from books."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='highlights'
    )
    book_id = models.IntegerField()
    chapter = models.ForeignKey(
        'books.Chapter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='highlights'
    )
    text = models.TextField()
    position_start = models.PositiveIntegerField()
    position_end = models.PositiveIntegerField()
    color = models.CharField(max_length=20, default='yellow')
    note = models.TextField(blank=True)
    page_number = models.PositiveIntegerField(null=True, blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Highlight')
        verbose_name_plural = _('Highlights')
    
    def __str__(self):
        return f"{self.user.email} - {self.text[:50]}..."


class Note(models.Model):
    """User notes from books."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    book_id = models.IntegerField()
    chapter = models.ForeignKey(
        'books.Chapter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notes'
    )
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    page_number = models.PositiveIntegerField(null=True, blank=True)
    highlight = models.ForeignKey(
        Highlight,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notes'
    )
    is_public = models.BooleanField(default=False)
    is_spoiler = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')
    
    def __str__(self):
        return f"{self.user.email} - {self.title or self.content[:50]}"


class Bookmark(models.Model):
    """User bookmarks in books."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    book_id = models.IntegerField()
    chapter = models.ForeignKey(
        'books.Chapter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookmarks'
    )
    page_number = models.PositiveIntegerField()
    position = models.PositiveIntegerField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'book_id', 'chapter']
        verbose_name = _('Bookmark')
        verbose_name_plural = _('Bookmarks')
    
    def __str__(self):
        return f"{self.user.email} - Book {self.book_id} at {self.page_number}"
