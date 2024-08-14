from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES=[
        ('male','male'),
        ('female','female'),
        ('others','others'),
        ('NA','NA'),
    ]
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    mobilenumber=models.CharField(max_length=100,blank=True,null=True)
    gender=models.CharField(max_length=30, choices=GENDER_CHOICES,default="NA")
    
    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['firstname','lastname',]

    def __str__(self):
        return str(self.email)

