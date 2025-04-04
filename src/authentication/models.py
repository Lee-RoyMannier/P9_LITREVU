from django.contrib.auth.models import AbstractUser
from django.db import models


class UserCustom(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, null=True)


class UserFollows(models.Model):
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(UserCustom, on_delete=models.CASCADE, related_name="followed_by")

    class Meta:
        unique_together = ("user", "followed_user")

    def is_following(self, user):
        return UserFollows.objects.filter(user=self, followed_user=user).exists()