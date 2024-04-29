import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Changed at")
    is_deleted = models.BooleanField(default=False, verbose_name="Is deleted")

    class Meta:
        abstract = True
