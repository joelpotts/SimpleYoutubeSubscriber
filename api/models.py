from django.contrib.auth.models import User
from django.db import models


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.CharField(max_length=200)

    class Meta:
        unique_together = ('user', 'channel',)

    def __str__(self):
        return f"{self.user.username}, {self.channel}"