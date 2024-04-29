from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission

from rest_framework import permissions

from apps.common.models import BaseModel
from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=150, blank=False, null=False, unique=True, verbose_name="Имя пользователя")
    email = models.EmailField(null=True, verbose_name="E-mail")
    password = models.CharField(max_length=128, blank=True, null=True, verbose_name="Пароль")
    otp = models.CharField(max_length=4, null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    is_admin = models.BooleanField(default=False, verbose_name="Админ")
    groups = models.ManyToManyField(Group, related_name="custom_user_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions")

    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    time = models.DateTimeField()


class IsAdminUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the admin user.
        return request.user.is_admin