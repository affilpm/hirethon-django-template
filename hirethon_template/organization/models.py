from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils.crypto import get_random_string

User = get_user_model()

# Create your models here.
class Role(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    EDITOR = 'editor', 'Editor'
    VIEWER = 'viewer', 'Viewer'
    
    
class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_organizations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.VIEWER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'organization')


class Namespace(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='namespaces')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_namespaces')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization.name} - {self.name}"


class ShortURL(models.Model):
    namespace = models.ForeignKey(Namespace, on_delete=models.CASCADE, related_name='short_urls')
    original_url = models.URLField()
    short_code = models.CharField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='short_urls')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('namespace', 'short_code')

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = get_random_string(6)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.namespace.name}/{self.short_code}"


class BulkUpload(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='bulk_uploads')
    namespace = models.ForeignKey(Namespace, on_delete=models.CASCADE, related_name='bulk_uploads')
    file = models.FileField(upload_to='uploads/' )  
    processed_file = models.FileField(upload_to='processed/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ], default='pending')    
    
    