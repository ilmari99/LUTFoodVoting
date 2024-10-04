from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'date')  # One vote per day
