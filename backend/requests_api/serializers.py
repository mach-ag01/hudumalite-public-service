from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import ServiceRequest, RequestStatusHistory
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')
    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        if not attrs.get('email'):
            raise serializers.ValidationError({'email': 'Email address is required.'})
        return attrs
    def create(self, validated_data):
        password = validated_data.pop('password')
        return User.objects.create_user(password=password, **validated_data)

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')

class RequestHistorySerializer(serializers.ModelSerializer):
    changed_by_name = serializers.SerializerMethodField()
    new_status_label = serializers.CharField(source='get_new_status_display', read_only=True)
    old_status_label = serializers.CharField(source='get_old_status_display', read_only=True)
    class Meta:
        model = RequestStatusHistory
        fields = ('id', 'old_status', 'new_status', 'old_status_label', 'new_status_label', 'note', 'changed_at', 'changed_by_name')
    def get_changed_by_name(self, obj):
        if not obj.changed_by: return 'System'
        return obj.changed_by.get_full_name() or obj.changed_by.username

class ServiceRequestSerializer(serializers.ModelSerializer):
    citizen_name = serializers.SerializerMethodField()
    category_label = serializers.CharField(source='get_category_display', read_only=True)
    status_label = serializers.CharField(source='get_status_display', read_only=True)
    image_url = serializers.SerializerMethodField()
    history = RequestHistorySerializer(many=True, read_only=True)
    class Meta:
        model = ServiceRequest
        fields = ('id', 'reference', 'citizen', 'citizen_name', 'title', 'category', 'category_label', 'location', 'description', 'image', 'image_url', 'status', 'status_label', 'staff_note', 'created_at', 'updated_at', 'resolved_at', 'history')
        read_only_fields = ('id', 'reference', 'citizen', 'status', 'staff_note', 'created_at', 'updated_at', 'resolved_at', 'history')
    def get_citizen_name(self, obj):
        return obj.citizen.get_full_name() or obj.citizen.username

def get_image_url(self, obj):
    if not obj.image:
        return None

    request = self.context.get('request')
    try:
        url = obj.image.url
    except (ValueError, OSError):
        return None

    if request:
        return request.build_absolute_uri(url)

    return url

    def validate_image(self, value):
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Image must be 5 MB or smaller.')
        if value and value.content_type not in ('image/jpeg', 'image/png', 'image/webp'):
            raise serializers.ValidationError('Upload a JPG, PNG, or WebP image.')
        return value

class StatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=ServiceRequest.Status.choices)
    staff_note = serializers.CharField(required=False, allow_blank=True, max_length=500)
