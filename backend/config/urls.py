from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from requests_api.views import RegisterView, MeView, RequestListCreateView, RequestDetailView, RequestStatusView, RequestHistoryView, AnalyticsView, HealthView

class RateLimitedTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    throttle_scope = 'login'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', HealthView.as_view(), name='health'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/token/', RateLimitedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/me/', MeView.as_view(), name='me'),
    path('api/requests/', RequestListCreateView.as_view(), name='request-list-create'),
    path('api/requests/<int:pk>/', RequestDetailView.as_view(), name='request-detail'),
    path('api/requests/<int:pk>/status/', RequestStatusView.as_view(), name='request-status'),
    path('api/requests/<int:pk>/history/', RequestHistoryView.as_view(), name='request-history'),
    path('api/analytics/', AnalyticsView.as_view(), name='analytics'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
