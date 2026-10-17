import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='ServiceRequest', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('reference', models.CharField(db_index=True, editable=False, max_length=16, unique=True)),
            ('title', models.CharField(max_length=120)),
            ('category', models.CharField(choices=[('roads','Roads & Potholes'),('water','Water Supply'),('lighting','Street Lighting'),('waste','Waste Collection'),('drainage','Drainage & Flooding'),('other','Other')], max_length=20)),
            ('location', models.CharField(max_length=180)),
            ('description', models.TextField(max_length=2000)),
            ('image', models.ImageField(blank=True, null=True, upload_to='service-requests/%Y/%m/')),
            ('status', models.CharField(choices=[('pending','Pending'),('in_progress','In Progress'),('resolved','Resolved')], db_index=True, default='pending', max_length=20)),
            ('staff_note', models.CharField(blank=True, max_length=500)),
            ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
            ('updated_at', models.DateTimeField(auto_now=True)),
            ('resolved_at', models.DateTimeField(blank=True, null=True)),
            ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='RequestStatusHistory', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('old_status', models.CharField(blank=True, choices=[('pending','Pending'),('in_progress','In Progress'),('resolved','Resolved')], max_length=20)),
            ('new_status', models.CharField(choices=[('pending','Pending'),('in_progress','In Progress'),('resolved','Resolved')], max_length=20)),
            ('note', models.CharField(blank=True, max_length=500)),
            ('changed_at', models.DateTimeField(auto_now_add=True)),
            ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='requests_api.servicerequest')),
        ], options={'ordering':['-changed_at']}),
    ]
