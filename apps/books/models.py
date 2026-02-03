from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Category(models.Model):
    """Category model for organizing books."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    icon = models.ImageField(upload_to='categories/icons/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Author(models.Model):
    """Author model for book creators."""
    user_id = models.IntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/photos/', null=True, blank=True)
    website = models.URLField(max_length=200, blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    total_books = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Book model for ebooks."""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PENDING_REVIEW = 'pending_review', _('Pending Review')
        APPROVED = 'approved', _('Approved')
        PUBLISHED = 'published', _('Published')
        REJECTED = 'rejected', _('Rejected')
        ARCHIVED = 'archived', _('Archived')
    
    class Format(models.TextChoices):
        EPUB = 'epub', _('EPUB')
        MOBI = 'mobi', _('MOBI')
        PDF = 'pdf', _('PDF')
        AUDIOBOOK = 'audiobook', _('Audiobook')
    
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    subtitle = models.CharField(max_length=500, blank=True)
    description = models.TextField()
    authors = models.ManyToManyField(Author, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books')
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    is_free = models.BooleanField(default=False)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_start = models.DateTimeField(null=True, blank=True)
    discount_end = models.DateTimeField(null=True, blank=True)
    
    # Book details
    format = models.CharField(max_length=20, choices=Format.choices, default=Format.EPUB)
    language = models.CharField(max_length=10, default='en')
    isbn = models.CharField(max_length=20, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    
    # Content
    pages = models.PositiveIntegerField(default=0)
    word_count = models.PositiveIntegerField(default=0)
    reading_time_hours = models.PositiveIntegerField(default=0)
    
    # Cover and preview
    cover_image = models.ImageField(upload_to='books/covers/', null=True, blank=True)
    preview_chapter = models.ForeignKey(
        'Chapter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preview_for'
    )
    sample_content = models.TextField(blank=True)
    
    # Metadata
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False)
    is_explicit = models.BooleanField(default=False)
    requires_adult_verification = models.BooleanField(default=False)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Files
    content_file = models.FileField(upload_to='books/files/', null=True, blank=True)
    encryption_key = models.CharField(max_length=256, blank=True)
    
    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def effective_price(self):
        if self.is_free:
            return 0
        if self.discount_price and self.discount_start and self.discount_end:
            now = timezone.now()
            if self.discount_start <= now <= self.discount_end:
                return self.discount_price
        return self.price


class Chapter(models.Model):
    """Chapter model for book content organization."""
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='chapters'
    )
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    word_count = models.PositiveIntegerField(default=0)
    is_free = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')
        ordering = ['order']
        unique_together = ['book', 'slug']
    
    def __str__(self):
        return f"{self.book.title} - {self.title}"


from django.utils import timezone

class BookFile(models.Model):
    """Model for book file versions and formats."""
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='files'
    )
    format = models.CharField(max_length=20, choices=Book.Format.choices)
    file = models.FileField(upload_to='books/files/')
    size = models.BigIntegerField(default=0)  # in bytes
    checksum = models.CharField(max_length=64, blank=True)
    version = models.CharField(max_length=20, default='1.0')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Book File')
        verbose_name_plural = _('Book Files')
    
    def __str__(self):
        return f"{self.book.title} ({self.format})"
    
    @property
    def size_mb(self):
        return round(self.size / (1024 * 1024), 2)
