"""
URL configuration for readerscent project.

Central URL router that includes all app-level URL configurations.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API Authentication
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # App APIs
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/books/', include('apps.books.urls')),
    path('api/v1/reader/', include('apps.reader.urls')),
    path('api/v1/marketplace/', include('apps.marketplace.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/reviews/', include('apps.reviews.urls')),
    path('api/v1/community/', include('apps.community.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/moderation/', include('apps.moderation.urls')),
    
    # Health check
    path('health/', include('django.contrib.auth.urls')),  # Placeholder for health checks
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
