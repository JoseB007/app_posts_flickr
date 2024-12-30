from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    
    def get_image(self):
        if self.image:
            avatar = self.image.url
        else:
            avatar = '/static/img/avatars/default.jpg'
        return avatar
    
    def get_full_name(self):
        if self.full_name:
            full_name = self.full_name
        else:
            full_name = self.user.username
        return full_name 
    
    def get_absolute_url(self):
        return reverse('profile:user-profile', args=[self.user.username])