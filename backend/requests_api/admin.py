from django.contrib import admin
from .models import ServiceRequest, RequestStatusHistory

class HistoryInline(admin.TabularInline):
    model = RequestStatusHistory
    extra = 0
    readonly_fields = ('changed_by', 'old_status', 'new_status', 'note', 'changed_at')
    can_delete = False

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('reference', 'title', 'category', 'citizen', 'location', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('reference', 'title', 'location', 'citizen__username', 'citizen__email')
    readonly_fields = ('reference', 'created_at', 'updated_at', 'resolved_at')
    inlines = [HistoryInline]

@admin.register(RequestStatusHistory)
class RequestStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('request', 'old_status', 'new_status', 'changed_by', 'changed_at')
    list_filter = ('new_status', 'changed_at')
