from rest_framework import serializers
from .models import Category, Author, Book, Chapter, BookFile


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'children', 'icon', 'is_active', 'order']
        read_only_fields = ['id']
    
    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return CategorySerializer(children, many=True).data


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author model."""
    
    class Meta:
        model = Author
        fields = [
            'id', 'user_id', 'name', 'slug', 'bio', 'photo', 'website',
            'social_links', 'total_books', 'total_sales', 'average_rating',
            'is_verified', 'is_featured', 'created_at'
        ]
        read_only_fields = ['id', 'total_books', 'total_sales', 'average_rating', 'created_at']


class ChapterSerializer(serializers.ModelSerializer):
    """Serializer for Chapter model."""
    
    class Meta:
        model = Chapter
        fields = [
            'id', 'title', 'slug', 'content', 'order', 'word_count',
            'is_free', 'is_published', 'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'word_count', 'created_at', 'updated_at']


class ChapterDetailSerializer(ChapterSerializer):
    """Detailed serializer for Chapter."""
    pass


class BookFileSerializer(serializers.ModelSerializer):
    """Serializer for BookFile model."""
    size_mb = serializers.ReadOnlyField()
    
    class Meta:
        model = BookFile
        fields = ['id', 'format', 'file', 'size', 'size_mb', 'checksum', 'version', 'is_active', 'created_at']
        read_only_fields = ['id', 'size', 'checksum', 'version', 'created_at']


class BookListSerializer(serializers.ModelSerializer):
    """Serializer for Book list view."""
    authors = AuthorSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    effective_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'subtitle', 'authors', 'categories',
            'cover_image', 'price', 'effective_price', 'is_free',
            'format', 'language', 'pages', 'average_rating', 'total_reviews',
            'view_count', 'is_featured', 'published_at'
        ]
        read_only_fields = ['id', 'view_count', 'total_reviews', 'published_at']


class BookDetailSerializer(BookListSerializer):
    """Detailed serializer for Book."""
    chapters = ChapterSerializer(many=True, read_only=True)
    files = BookFileSerializer(many=True, read_only=True)
    
    class Meta(BookListSerializer.Meta):
        fields = BookListSerializer.Meta.fields + [
            'description', 'isbn', 'publisher', 'publication_date',
            'word_count', 'reading_time_hours', 'preview_chapter', 'sample_content',
            'status', 'is_explicit', 'requires_adult_verification',
            'download_count', 'chapters', 'files', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'download_count', 'chapters', 'files', 'created_at', 'updated_at']


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating Book."""
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all())
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    
    class Meta:
        model = Book
        fields = [
            'title', 'slug', 'subtitle', 'description', 'authors', 'categories',
            'price', 'currency', 'is_free', 'discount_price', 'discount_start', 'discount_end',
            'format', 'language', 'isbn', 'publisher', 'publication_date',
            'pages', 'word_count', 'reading_time_hours', 'cover_image',
            'sample_content', 'status', 'is_featured', 'is_explicit',
            'requires_adult_verification', 'content_file'
        ]
    
    def validate(self, attrs):
        if attrs.get('discount_price') and not (attrs.get('discount_start') and attrs.get('discount_end')):
            raise serializers.ValidationError(
                "Discount start and end dates are required when discount_price is set."
            )
        return attrs
