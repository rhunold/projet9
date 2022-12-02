from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass


class UserFollow(models.Model):
    """Stores a unique pair auth.User """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by"
    )

    class Meta:
        unique_together = (
            "user",
            "followed_user",
        )

    def __str__(self):
        return f"{self.user}, {self.followed_user}"
