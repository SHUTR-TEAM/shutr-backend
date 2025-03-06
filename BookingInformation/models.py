from djongo import models

class BookingInformation(models.Model):
    id = models.ObjectIdField(primary_key=True)
    status = models.CharField(max_length=20)
    client = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    time = models.CharField(max_length=20) 

    def __str__(self):
        return f"{self.client} - {self.category} - {self.status}"
