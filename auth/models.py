# from django.db import models
# from django import models as djongo_models

# class Customer(djongo_models.Model):
#     email = models.EmailField(primary_key=True)
#     name = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)

#     class Meta:
#         abstract = True

# class Photographer(Customer):
#     username = models.CharField(max_length=100, unique=True)
#     id_number = models.CharField(max_length=50)
#     bank_account = models.CharField(max_length=50)
#     id_verification = models.FileField(upload_to='id_verifications/')

#     def __str__(self):
#         return self.username