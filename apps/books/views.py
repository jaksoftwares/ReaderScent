from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import Category, Author, Book, Chapter, BookFile
from .serializers import (
    CategorySerializer, AuthorSerializer,
    BookListSerializer, BookDetailSerializer, BookCreateUpdateSerializer,
    ChapterSerializer, BookFileSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Category CRUD operations."""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        parent_id = self.request.query_params.get('parent')
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        return queryset


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet for Author CRUD operations."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def books(self, request, slug=None):
        author = self.get_object()
        books = author.books.filter(status=Book.Status.PUBLISHED)
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for Book CRUD operations."""
    queryset = Book.objects.all()
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        elif self.action == 'retrieve':
            return BookDetailSerializer
        return BookCreateUpdateSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        else:
            queryset = queryset.filter(status=Book.Status.PUBLISHED)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(categories__slug=category)
        
        # Filter by author
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(authors__slug=author)
        
        # Filter by format
        format_filter = self.request.query_params.get('format')
        if format_filter:
            queryset = queryset.filter(format=format_filter)
        
        # Filter by price (free or paid)
        is_free = self.request.query_params.get('is_free')
        if is_free and is_free.lower() == 'true':
            queryset = queryset.filter(is_free=True)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        # Ordering
        ordering = self.request.query_params.get('ordering', '-published_at')
        valid_orderings = ['title', '-title', 'price', '-price', 'average_rating', 
                          '-average_rating', 'published_at', '-published_at', 
                          'view_count', '-view_count', 'created_at', '-created_at']
        if ordering in valid_orderings:
            queryset = queryset.order_by(ordering)
        
        return queryset.distinct()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        Book.objects.filter(id=instance.id).update(view_count=F('view_count') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def chapters(self, request, slug=None):
        book = self.get_object()
        chapters = book.chapters.filter(is_published=True).order_by('order')
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def chapter(self, request, slug=None, chapter_slug=None):
        book = self.get_object()
        chapter = get_object_or_404(Chapter, book=book, slug=chapter_slug)
        serializer = ChapterSerializer(chapter)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def submit_for_review(self, request, slug=None):
        book = self.get_object()
        if book.status != Book.Status.DRAFT:
            return Response(
                {"error": "Only draft books can be submitted for review."},
                status=status.HTTP_400_BAD_REQUEST
            )
        book.status = Book.Status.PENDING_REVIEW
        book.save()
        return Response(BookDetailSerializer(book).data)


class ChapterViewSet(viewsets.ModelViewSet):
    """ViewSet for Chapter CRUD operations."""
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        book_slug = self.kwargs.get('book_slug')
        if book_slug:
            queryset = queryset.filter(book__slug=book_slug)
        return queryset


class BookFileViewSet(viewsets.ModelViewSet):
    """ViewSet for BookFile CRUD operations."""
    queryset = BookFile.objects.all()
    serializer_class = BookFileSerializer
