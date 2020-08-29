from django.contrib.auth.models import User
from django.db import models


class CommitteeMember(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    committee = models.CharField(max_length=100, default="")
    teacher_id = models.CharField(max_length=100, default="")
    college = models.CharField(max_length=100, default="")
    is_approved = models.BooleanField(default="False")
    phone_no = models.CharField(max_length=10, default="")
    pending_request = models.CharField(max_length=1000, default="")
    gender = models.CharField(max_length=10,default="")
    dob = models.CharField(max_length=10,default="")
    branch = models.CharField(max_length=30,default="")
    address = models.CharField(max_length=1000, default="")

class Otp(models.Model):
    phone_no = models.CharField(max_length=10, default="")
    otp_phone_no = models.CharField(max_length=6, default="")
    email = models.CharField(max_length=100, default="")
    otp_email = models.CharField(max_length=6, default="")
