from django.contrib.auth.backends import BaseBackend

from .models import User


class AccountBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user: User = User._default_manager.get_by_natural_key(username)
        except User.DoesNotExist:
            return

        if user.check_password(password) and user.is_active:
            return user

    def get_user(self, user_id):
        try:
            user = User._default_manager.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if user.is_active else None

    def has_perm(self, user_obj, perm, obj=None):
        return user_obj.is_active and super().has_perm(user_obj, perm, obj=obj)
