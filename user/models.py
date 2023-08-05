from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class TypeUser(models.TextChoices):
        RESTAURANT = "Restaurant"
        EMPLOYEE = "Employee"

    type_of_user = models.CharField(max_length=50, choices=TypeUser.choices)
    votes = models.BooleanField(default=False)
