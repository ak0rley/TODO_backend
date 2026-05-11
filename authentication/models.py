from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['name', 'email']
    USERNAME_FIELD = 'username'