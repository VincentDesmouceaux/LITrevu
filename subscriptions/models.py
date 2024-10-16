from django.conf import settings
from django.db import models


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following_subscriptions'
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follower_subscriptions'
    )

    class Meta:
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f'{self.user} suit {self.followed_user}'
