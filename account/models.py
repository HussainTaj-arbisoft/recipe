from django.db import models
from django.contrib.auth.models import User


def _image_path(model, filename: str):
    return f'account/profile_image/{model.user.id}.{filename.split(".")[-1]}'


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField('Profile Picture', upload_to=_image_path)

    def __str__(self):
        return f'Profile: {self.user.username}'
