from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser, Profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name', 'role']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details."""
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'role',
            'avatar', 'bio', 'is_verified', 'is_premium',
            'date_of_birth', 'email_notifications', 'marketing_emails',
            'created_at', 'last_login'
        ]
        read_only_fields = ['id', 'email', 'is_verified', 'created_at', 'last_login']


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    email = serializers.EmailField(source='user.email', read_only=True)
    favorite_genres = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id', 'email', 'display_name', 'website', 'twitter',
            'facebook', 'linkedin', 'favorite_genres', 'reading_preferences',
            'social_connections', 'total_books_read', 'total_pages_read',
            'total_minutes_read', 'achievements', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'email', 'created_at', 'updated_at']


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for password reset request."""
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email doesn't exist")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation."""
    new_password = serializers.CharField(required=True, validators=[validate_password])
