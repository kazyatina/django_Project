import os

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from dotenv import load_dotenv

load_dotenv(override=True)
from django_countries.fields import CountryField


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Телефон"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар"
    )
    country = CountryField(max_length=50, blank=True, null=True, verbose_name="Страна")
    token = models.CharField(
        max_length=100, verbose_name="token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
