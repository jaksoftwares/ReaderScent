from django.contrib import admin
from .models import Category, Author, Book, Chapter, BookFile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'total_books', 'total_sales', 'average_rating', 'is_verified', 'is_featured')
    list_filter = ('is_verified', 'is_featured')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('total_books', 'total_sales', 'average_rating', 'created_at', 'updated_at')


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0
    prepopulated_fields = {'slug': ('title',)}


class BookFileInline(admin.TabularInline):
    model = BookFile
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'price', 'is_free', 'format', 'view_count', 'average_rating', 'published_at')
    list_filter = ('status', 'is_free', 'format', 'language', 'is_featured')
    search_fields = ('title', 'slug', 'authors__name')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('authors', 'categories')
    inlines = [ChapterInline, BookFileInline]
    readonly_fields = ('view_count', 'download_count', 'average_rating', 'total_reviews', 'created_at', 'updated_at')
    date_hierarchy = 'published_at'
    
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'subtitle', 'description')}),
        ('Authors & Categories', {'fields': ('authors', 'categories')}),
        ('Pricing', {'fields': ('price', 'currency', 'is_free', 'discount_price', 'discount_start', 'discount_end')}),
        ('Book Details', {'fields': ('format', 'language', 'isbn', 'publisher', 'publication_date', 'pages', 'word_count', 'reading_time_hours')}),
        ('Content', {'fields': ('cover_image', 'preview_chapter', 'sample_content', 'content_file')}),
        ('Status', {'fields': ('status', 'is_featured', 'is_explicit', 'requires_adult_verification')}),
        ('Analytics', {'fields': ('view_count', 'download_count', 'average_rating', 'total_reviews')}),
        ('Dates', {'fields': ('published_at',)}),
    )


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'order', 'word_count', 'is_free', 'is_published', 'published_at')
    list_filter = ('is_free', 'is_published')
    search_fields = ('title', 'book__title')
    readonly_fields = ('word_count', 'created_at', 'updated_at')


@admin.register(BookFile)
class BookFileAdmin(admin.ModelAdmin):
    list_display = ('book', 'format', 'size_mb', 'version', 'is_active', 'created_at')
    list_filter = ('format', 'is_active')
    readonly_fields = ('size', 'checksum', 'created_at')
