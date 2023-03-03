from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    email = models.CharField(max_length=127, unique=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField(null=True)
    is_employee = models.BooleanField(default=False)