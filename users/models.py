from django.utils.timezone import now

from django.contrib.auth.models import AbstractUser
from django.db import models


class SNUser(AbstractUser):
    last_activity = models.DateTimeField(default=now)
