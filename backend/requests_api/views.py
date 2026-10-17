from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ServiceRequest, RequestStatusHistory
from .serializers import RegisterSerializer, UserSummarySerializer, ServiceRequestSerializer, StatusUpdateSerializer, RequestHistorySerializer
User = get_user_model()

class HealthView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request): return Response({'status': 'ok', 'service': 'HudumaLite API'})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'register'

class MeView(APIView):
    def get(self, request): return Response(UserSummarySerializer(request.user).data)

class RequestListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def get_throttles(self):
        if self.request.method == 'POST':
            self.throttle_scope = 'request_create'
        else:
            self.throttle_scope = None
        return super().get_throttles()
    def get_queryset(self):
        qs = ServiceRequest.objects.select_related('citizen').prefetch_related('history__changed_by')
        if not self.request.user.is_staff: qs = qs.filter(citizen=self.request.user)
        status_filter = self.request.query_params.get('status')
        category_filter = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if status_filter: qs = qs.filter(status=status_filter)
        if category_filter: qs = qs.filter(category=category_filter)
        if search: qs = qs.filter(Q(reference__icontains=search) | Q(title__icontains=search) | Q(location__icontains=search) | Q(description__icontains=search))
        return qs.order_by('-created_at')
    def perform_create(self, serializer):
        obj = serializer.save(citizen=self.request.user)
        RequestStatusHistory.objects.create(request=obj, changed_by=self.request.user, old_status='', new_status=obj.status, note='Request submitted')

class RequestDetailView(generics.RetrieveAPIView):
    serializer_class = ServiceRequestSerializer
    def get_queryset(self):
        qs = ServiceRequest.objects.select_related('citizen').prefetch_related('history__changed_by')
        return qs if self.request.user.is_staff else qs.filter(citizen=self.request.user)

class RequestStatusView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def patch(self, request, pk):
        try: item = ServiceRequest.objects.get(pk=pk)
        except ServiceRequest.DoesNotExist: return Response({'detail': 'Request not found.'}, status=404)
        serializer = StatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data['status']
        note = serializer.validated_data.get('staff_note', '').strip()
        old_status = item.status
        item.status = new_status
        item.staff_note = note
        item.resolved_at = timezone.now() if new_status == ServiceRequest.Status.RESOLVED else None
        item.save(update_fields=['status', 'staff_note', 'resolved_at', 'updated_at'])
        if old_status != new_status or note:
            RequestStatusHistory.objects.create(request=item, changed_by=request.user, old_status=old_status, new_status=new_status, note=note or f'Status changed to {item.get_status_display()}')
        return Response(ServiceRequestSerializer(item, context={'request': request}).data)

class RequestHistoryView(generics.ListAPIView):
    serializer_class = RequestHistorySerializer
    def get_queryset(self):
        qs = RequestStatusHistory.objects.select_related('request', 'changed_by')
        return qs.filter(request_id=self.kwargs['pk']) if self.request.user.is_staff else qs.filter(request_id=self.kwargs['pk'], request__citizen=self.request.user)

class AnalyticsView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        qs = ServiceRequest.objects.all()
        counts = qs.values('status').annotate(count=Count('id'))
        by_status = {row['status']: row['count'] for row in counts}
        by_category = list(qs.values('category').annotate(count=Count('id')).order_by('-count'))
        recent = qs.order_by('-created_at').values('reference', 'title', 'category', 'status', 'created_at')[:5]
        total = qs.count()
        return Response({'total': total, 'pending': by_status.get('pending', 0), 'in_progress': by_status.get('in_progress', 0), 'resolved': by_status.get('resolved', 0), 'open': by_status.get('pending', 0) + by_status.get('in_progress', 0), 'by_status': by_status, 'by_category': by_category, 'recent': list(recent)})
