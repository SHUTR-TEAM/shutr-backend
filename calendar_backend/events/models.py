# from djongo import models

# class Event(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=200)
#     start = models.DateTimeField()
#     end = models.DateTimeField(null=True, blank=True)
#     all_day = models.BooleanField(default=False)

#     def __str__(self):
#         return self.title

from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
