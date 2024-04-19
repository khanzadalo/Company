from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission

from rest_framework import permissions

from main.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=150, blank=False, null=False, unique=True, verbose_name="Username")
    email = models.EmailField(null=True, verbose_name="E-mail")
    password = models.CharField(max_length=128, blank=True, null=True, verbose_name="Password")
    otp = models.CharField(max_length=4, null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name="Active")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    is_admin = models.BooleanField(default=False, verbose_name="Admin")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')
    groups = models.ManyToManyField(Group, related_name="custom_user_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions")
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    avatar = models.ImageField(null=True, blank=False, verbose_name="Avatar")

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "profile"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = "-created_at",


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    time = models.DateTimeField()


class IsAdminUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the admin user.
        return request.user.is_admin