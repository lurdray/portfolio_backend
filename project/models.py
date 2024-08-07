import uuid
from django.db import models
from django.utils import timezone


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    link = models.CharField(max_length=255)

    image = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="default_files/default_face.jpg")
    video = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="default_files/default_face.jpg")


    status = models.BooleanField(default=True)
    pub_date = models.DateTimeField(default=timezone.now)


    def __str__(self) -> str:
        return self.title

