import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

from project.models import Project

from django.utils import timezone

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    projects = models.ManyToManyField(Project, through="CustomUserProjectConnector")


class CustomUserProjectConnector(models.Model):
	custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)
