from django.db import models
from django.contrib.auth.models import User

# Create your models here. 

def upload_to(instance, filename):
    return f'profiles/{instance.user.id}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=upload_to, blank=True, null=True)
    background_image = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return self.user.username





