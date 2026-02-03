from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, AuthorViewSet, BookViewSet, ChapterViewSet, BookFileViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
    path('<slug:book_slug>/chapters/', include([
        path('', ChapterViewSet.as_view({'get': 'list'}), name='book-chapters'),
        path('<slug:chapter_slug>/', ChapterViewSet.as_view({'get': 'retrieve'}), name='book-chapter-detail'),
    ])),
    path('files/', BookFileViewSet.as_view({'get': 'list', 'post': 'create'}), name='bookfiles'),
]
