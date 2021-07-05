from django.db import models
import uuid
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField

from django.db.models.fields.related import ForeignKey

# Create your models here.


class Credential(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.UUIDField(default=uuid.uuid4, editable=True)


class Host(models.Model):
    hostname = models.CharField(max_length=32, unique=True)
    address = models.CharField(max_length=40)  # IPv6 max is 39
    updated = models.DateTimeField()
    user = ForeignKey(Credential, on_delete=CASCADE)
