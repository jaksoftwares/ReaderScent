from rest_framework import serializers
from .models import Review, Comment, Rating


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_email', 'book_id', 'rating', 'title',
            'content', 'is_spoiler', 'is_verified_purchase', 'helpful_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'helpful_count', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'user_email', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for Rating model."""
    
    class Meta:
        model = Rating
        fields = ['id', 'user', 'book_id', 'rating', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
