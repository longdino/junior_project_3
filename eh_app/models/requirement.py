from . import _BaseTimestampModel
from django.db import models

class Requirement(_BaseTimestampModel):
    class Meta:
        db_table = 'requirement'

    code = models.CharField(primary_key=True, max_length=16)
    description = models.TextField(max_length=255, default=None, null=True)
