from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, Wishlist, PromoCode
from decimal import Decimal


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem model."""
    
    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'quantity', 'added_at']
        read_only_fields = ['id', 'added_at']


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model."""
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_items', 'subtotal', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model."""
    
    class Meta:
        model = OrderItem
        fields = ['id', 'book_id', 'book_title', 'book_price', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'subtotal', 'discount', 'tax',
            'total', 'currency', 'payment_method', 'paid_at',
            'billing_address', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for Wishlist model."""
    books = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'books', 'created_at']
        read_only_fields = ['id', 'created_at']


class PromoCodeSerializer(serializers.ModelSerializer):
    """Serializer for PromoCode model."""
    is_valid = serializers.ReadOnlyField()
    
    class Meta:
        model = PromoCode
        fields = [
            'id', 'code', 'discount_type', 'discount_value', 'min_order_amount',
            'max_uses', 'current_uses', 'is_active', 'valid_from', 'valid_until',
            'is_valid', 'created_at'
        ]
        read_only_fields = ['id', 'current_uses', 'created_at']
