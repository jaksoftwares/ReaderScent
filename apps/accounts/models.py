from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for the CustomUser model."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Uses email as the primary identifier instead of username.
    """
    
    class Roles(models.TextChoices):
        READER = 'reader', _('Reader')
        AUTHOR = 'author', _('Author')
        MODERATOR = 'moderator', _('Moderator')
        ADMIN = 'admin', _('Admin')
    
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.READER
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    premium_since = models.DateTimeField(null=True, blank=True)
    last_read = models.DateTimeField(null=True, blank=True)
    email_notifications = models.BooleanField(default=True)
    marketing_emails = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=128, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'users'
    
    def __str__(self):
        return self.email
    
    @property
    def is_author(self):
        return self.role == self.Roles.AUTHOR or self.is_superuser
    
    @property
    def is_moderator(self):
        return self.role in [self.Roles.MODERATOR, self.Roles.ADMIN] or self.is_superuser


class Profile(models.Model):
    """
    Extended profile information for users.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    display_name = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    facebook = models.CharField(max_length=50, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    favorite_genres = models.ManyToManyField('books.Category', blank=True)
    reading_preferences = models.JSONField(default=dict, blank=True)
    social_connections = models.JSONField(default=dict, blank=True)
    total_books_read = models.IntegerField(default=0)
    total_pages_read = models.IntegerField(default=0)
    total_minutes_read = models.IntegerField(default=0)
    achievements = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
    
    def __str__(self):
        return f"Profile for {self.user.email}"
