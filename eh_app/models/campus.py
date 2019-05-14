from . import _BaseTimestampModel
from django.db import models

class Campus(_BaseTimestampModel):
    class Meta:
        db_table = 'campus'

    name = models.CharField(primary_key=True, max_length=3)
    description = models.CharField(max_length=45, default=None, null=True)
