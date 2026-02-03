from rest_framework import serializers
from .models import ReadingProgress, Highlight, Note, Bookmark


class ReadingProgressSerializer(serializers.ModelSerializer):
    """Serializer for ReadingProgress model."""
    
    class Meta:
        model = ReadingProgress
        fields = [
            'id', 'book_id', 'current_page', 'current_chapter',
            'percent_complete', 'last_position', 'last_read_at',
            'started_at', 'finished_at'
        ]
        read_only_fields = ['id', 'last_read_at', 'started_at']


class HighlightSerializer(serializers.ModelSerializer):
    """Serializer for Highlight model."""
    
    class Meta:
        model = Highlight
        fields = [
            'id', 'book_id', 'chapter', 'text', 'position_start',
            'position_end', 'color', 'note', 'page_number',
            'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note model."""
    
    class Meta:
        model = Note
        fields = [
            'id', 'book_id', 'chapter', 'title', 'content',
            'page_number', 'highlight', 'is_public', 'is_spoiler',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookmarkSerializer(serializers.ModelSerializer):
    """Serializer for Bookmark model."""
    
    class Meta:
        model = Bookmark
        fields = [
            'id', 'book_id', 'chapter', 'page_number', 'position',
            'note', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
