from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    place = models.CharField(max_length=100)    
    phone = models.CharField(max_length=15)
    LOGIN=models.OneToOneField(User,on_delete=models.CASCADE)

class ChatBot(models.Model):
    question=models.TextField()
    answer=models.TextField()
    datetime=models.DateTimeField()
    USER=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
