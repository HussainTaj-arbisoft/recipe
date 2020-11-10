from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    email = models.EmailField("email address", unique=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super().save(args, kwargs)
        try:
            self.profile = self.profile
        except Profile.DoesNotExist:
            self.profile = Profile()
        self.profile.save()


def _image_path(model, filename: str):
    return f'media/account/profile_image/{model.user.id}.{filename.split(".")[-1]}'


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    image = models.ImageField("Profile Picture", upload_to=_image_path)

    def __str__(self):
        return f"Profile: {self.user.username}"

    def get_image_or_default_url(self):
        if self.image:
            return self.image
        return "static/account/profile_image/placeholder.png"
