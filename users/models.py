# users/models.py
import uuid
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from users import manager


class CustomUser(AbstractUser):
    gender_choices = (
        ('male', 'male'),
        ('female', 'female')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gender = models.CharField(null=True, blank=False, choices=gender_choices, max_length=10)
    age = models.IntegerField(null=True, blank=False)
    register_completed = models.BooleanField(default=False)
    objects = UserManager()
    active = manager.ActiveManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
        ordering = ('date_joined',)
        indexes = [
            models.Index(fields=['id'], name='user_id'),
            models.Index(fields=['username'], name='user_username')
        ]


class UserHolidays(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)

    name = models.TextField(null=False, blank=True)
    name_local = models.CharField(null=False, blank=True, max_length=255)
    language = models.CharField(null=False, blank=True, max_length=64)
    description = models.TextField(null=False, blank=True)
    country = models.CharField(null=False, blank=True, max_length=128)
    location = models.TextField(null=False, blank=True)
    type = models.CharField(null=False, blank=True, max_length=255)
    date = models.CharField(null=False, blank=True, max_length=64)
    date_year = models.CharField(null=False, blank=True, max_length=4)
    date_month = models.CharField(null=False, blank=True, max_length=2)
    date_day = models.CharField(null=False, blank=True, max_length=2)
    week_day = models.CharField(null=False, blank=True, max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.name}'

    class Meta:
        db_table = 'user_holidays'
        ordering = ('updated_at',)
        indexes = [
            models.Index(fields=['id'], name='holidays_id'),
            models.Index(fields=['country'], name='country')
        ]
