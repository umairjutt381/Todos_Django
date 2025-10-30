from django.contrib.auth.models import User
from django.db import models

class DashboardImage(models.Model):
    image = models.ImageField(upload_to='dashboard_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)
    location = models.CharField(max_length=120,blank=True,null=True)

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    task_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)