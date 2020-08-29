from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class student(models.Model):
    user = models.OneToOneField(User,models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_picture/', default='profile_picture/IMG_1520.JPG')
    college_id = models.CharField(max_length=100, default="")
    dob= models.CharField(max_length=20, default="")
    gender= models.CharField(max_length=20, default="")
    college_name = models.CharField(max_length=100, default="")
    branch = models.CharField(max_length=100, default="")
    phone_no = models.CharField(max_length=10, default="")
    address =  models.CharField(max_length=100, default="")
    liked_complaint = models.CharField(max_length=1000, default="")
    post_ids = models.CharField(max_length=1000, default="")



