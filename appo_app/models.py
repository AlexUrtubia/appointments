from django.db import models
from django.db.models.deletion import CASCADE
from login.models import User

# Create your models here.
class Appointment(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=7)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="appointments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
