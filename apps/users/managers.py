from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, username, is_admin, is_staff, is_active, password=None):
        if not username:
            raise ValueError("User must have an username")
        user = self.model(
            username=username,
            is_admin=is_admin,
            is_active=is_active,
            is_staff=is_staff,
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password=None):
        return self._create_user(
            username=username,
            is_admin=False,
            is_staff=False,
            is_active=True,
            password=password,
        )

    def create_admin(self, username, password=None):
        return self._create_user(
            username=username,
            is_admin=True,
            is_staff=True,
            is_active=True,
            password=password,
        )
