from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class Transaction(models.Model):
    """Model for tracking all payment transactions."""
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PROCESSING = 'processing', _('Processing')
        COMPLETED = 'completed', _('Completed')
        FAILED = 'failed', _('Failed')
        REFUNDED = 'refunded', _('Refunded')
        CANCELLED = 'cancelled', _('Cancelled')
    
    class Type(models.TextChoices):
        PAYMENT = 'payment', _('Payment')
        REFUND = 'refund', _('Refund')
        PAYOUT = 'payout', _('Payout')
        DEPOSIT = 'deposit', _('Deposit')
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    order = models.ForeignKey(
        'marketplace.Order',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='transactions'
    )
    transaction_type = models.CharField(max_length=20, choices=Type.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=50, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=128, blank=True)
    stripe_charge_id = models.CharField(max_length=128, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
    
    def __str__(self):
        return f"{self.transaction_type} - {self.amount} {self.currency}"


class Wallet(models.Model):
    """User wallet for storing earnings."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    pending_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='USD')
    stripe_account_id = models.CharField(max_length=128, blank=True)
    stripe_account_status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')
    
    def __str__(self):
        return f"Wallet for {self.user.email} - {self.balance} {self.currency}"


class Payout(models.Model):
    """Model for author payouts."""
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PROCESSING = 'processing', _('Processing')
        COMPLETED = 'completed', _('Completed')
        FAILED = 'failed', _('Failed')
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='payouts'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payout_method = models.CharField(max_length=50, blank=True)
    stripe_transfer_id = models.CharField(max_length=128, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Payout')
        verbose_name_plural = _('Payouts')
    
    def __str__(self):
        return f"Payout {self.id} - {self.amount} {self.currency}"


class Royalty(models.Model):
    """Model for tracking author royalties."""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='royalties'
    )
    book_id = models.IntegerField()
    book_title = models.CharField(max_length=500)
    order = models.ForeignKey(
        'marketplace.Order',
        on_delete=models.PROTECT,
        related_name='royalties'
    )
    quantity = models.PositiveIntegerField(default=1)
    list_price = models.DecimalField(max_digits=10, decimal_places=2)
    royalty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('70.00'))  # Percentage
    royalty_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=Payout.Status.choices, default=Payout.Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Royalty')
        verbose_name_plural = _('Royalties')
    
    def __str__(self):
        return f"Royalty for {self.author.email} - {self.book_title}"
