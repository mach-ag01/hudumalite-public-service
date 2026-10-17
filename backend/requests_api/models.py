import uuid
from django.conf import settings
from django.db import models

class ServiceRequest(models.Model):
    class Category(models.TextChoices):
        ROADS = 'roads', 'Roads & Potholes'
        WATER = 'water', 'Water Supply'
        LIGHTING = 'lighting', 'Street Lighting'
        WASTE = 'waste', 'Waste Collection'
        DRAINAGE = 'drainage', 'Drainage & Flooding'
        OTHER = 'other', 'Other'
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
    reference = models.CharField(max_length=16, unique=True, editable=False, db_index=True)
    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_requests')
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=Category.choices)
    location = models.CharField(max_length=180)
    description = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='service-requests/%Y/%m/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    staff_note = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f'HD-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.reference} — {self.title}'

class RequestStatusHistory(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='history')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    old_status = models.CharField(max_length=20, choices=ServiceRequest.Status.choices, blank=True)
    new_status = models.CharField(max_length=20, choices=ServiceRequest.Status.choices)
    note = models.CharField(max_length=500, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-changed_at']
    def __str__(self):
        return f'{self.request.reference}: {self.old_status} → {self.new_status}'
