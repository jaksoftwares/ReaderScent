from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewViewSet, AnalyticsDashboardView

router = DefaultRouter()
router.register(r'views', BookViewViewSet, basename='bookview')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
]
