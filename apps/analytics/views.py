from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from datetime import timedelta
from .models import BookView, PageView, DailyAnalytics, UserAnalytics


class BookViewViewSet(viewsets.ModelViewSet):
    """ViewSet for tracking book views."""
    queryset = BookView.objects.all()
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        BookView.objects.create(
            book_id=request.data.get('book_id'),
            user=request.user if request.user.is_authenticated else None,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            referrer=request.META.get('HTTP_REFERER', '')
        )
        return Response({"status": "tracked"})
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class AnalyticsDashboardView(views.APIView):
    """Analytics dashboard for admins."""
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        
        data = {
            'today_views': BookView.objects.filter(timestamp__date=today).count(),
            'week_views': BookView.objects.filter(timestamp__date__gte=week_ago).count(),
            'total_users': 0,
            'total_books': 0,
        }
        return Response(data)
