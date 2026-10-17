from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import ServiceRequest, RequestStatusHistory
User = get_user_model()

class RequestApiTests(TestCase):
    def setUp(self):
        self.citizen = User.objects.create_user(username='citizen1', password='Test-pass-9381', email='citizen@example.com')
        self.other = User.objects.create_user(username='citizen2', password='Test-pass-9381', email='other@example.com')
        self.staff = User.objects.create_superuser(username='officer', password='Test-pass-9381', email='officer@example.com')
        self.client = APIClient()
    def test_citizen_can_create_request(self):
        self.client.force_authenticate(self.citizen)
        response = self.client.post('/api/requests/', {'title':'Broken streetlight','category':'lighting','location':'Kenyatta Avenue','description':'Lamp is not working'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['reference'].startswith('HD-'))
        self.assertEqual(ServiceRequest.objects.count(), 1)
        self.assertEqual(RequestStatusHistory.objects.count(), 1)
    def test_citizen_only_sees_own_requests(self):
        ServiceRequest.objects.create(citizen=self.other, title='Water issue', category='water', location='Estate A', description='No water')
        self.client.force_authenticate(self.citizen)
        response = self.client.get('/api/requests/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)
    def test_only_staff_can_update_status(self):
        item = ServiceRequest.objects.create(citizen=self.citizen, title='Road damage', category='roads', location='Road B', description='Large pothole')
        self.client.force_authenticate(self.citizen)
        denied = self.client.patch(f'/api/requests/{item.pk}/status/', {'status':'resolved'}, format='json')
        self.assertEqual(denied.status_code, 403)
        self.client.force_authenticate(self.staff)
        allowed = self.client.patch(f'/api/requests/{item.pk}/status/', {'status':'in_progress','staff_note':'Crew assigned'}, format='json')
        self.assertEqual(allowed.status_code, 200)
        item.refresh_from_db()
        self.assertEqual(item.status, 'in_progress')
