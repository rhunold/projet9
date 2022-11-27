from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass
    # profile_photo = models.ImageField(verbose_name='Photo de profil')
    
#     CREATOR = 'CREATOR'
#     SUBSCRIBER = 'SUBSCRIBER'

# ROLE_CHOICES = (
#     (CREATOR, 'Créateur'),
#     (SUBSCRIBER, 'Abonné'),
# )
    # role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
    
    
class UserFollow(models.Model):
    """Stores a unique pair of :model:`auth.User`."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by"
    )

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = (
            "user",
            "followed_user",
        )

    def __str__(self):
        return f"{self.user}, {self.followed_user}"    