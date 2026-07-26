from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_username_not_me


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(regex=r'^[\w.@+-]+\Z'),
            validate_username_not_me,
        ]
    )
    email = models.EmailField('Email адрес', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role in Role.values),
        choices=Role.choices,
        default=Role.USER
    )
    confirmation_code = models.CharField(
        max_length=100, blank=True, null=True
    )

    @property
    def is_admin(self):
        return (
            self.role == self.Role.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
