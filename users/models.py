from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles(models.TextChoices):
    USER = 'User'
    MODERATOR = 'Moderator'


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    role = models.CharField(max_length=15, choices=UserRoles.choices, default=UserRoles.USER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
