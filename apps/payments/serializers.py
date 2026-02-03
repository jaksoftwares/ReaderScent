from rest_framework import serializers
from .models import Transaction, Wallet, Payout, Royalty


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'order', 'transaction_type', 'status', 'amount',
            'currency', 'payment_method', 'stripe_payment_intent_id',
            'metadata', 'error_message', 'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WalletSerializer(serializers.ModelSerializer):
    """Serializer for Wallet model."""
    
    class Meta:
        model = Wallet
        fields = [
            'id', 'user', 'balance', 'pending_balance', 'currency',
            'stripe_account_id', 'stripe_account_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class PayoutSerializer(serializers.ModelSerializer):
    """Serializer for Payout model."""
    
    class Meta:
        model = Payout
        fields = [
            'id', 'user', 'amount', 'currency', 'status', 'payout_method',
            'stripe_transfer_id', 'notes', 'created_at', 'updated_at', 'processed_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RoyaltySerializer(serializers.ModelSerializer):
    """Serializer for Royalty model."""
    
    class Meta:
        model = Royalty
        fields = [
            'id', 'author', 'book_id', 'book_title', 'order', 'quantity',
            'list_price', 'royalty_rate', 'royalty_amount', 'currency',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
