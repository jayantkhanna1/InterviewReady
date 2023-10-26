from django.db import models 

class User(models.Model):
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    otp = models.CharField(max_length=200)
    otp_verified = models.BooleanField(default=False)
    private_key = models.CharField(max_length=200)