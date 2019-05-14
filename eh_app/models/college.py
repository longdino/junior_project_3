from . import _BaseTimestampModel
from django.db import models

class College(_BaseTimestampModel):
    class Meta:
        db_table = 'college'

    name = models.CharField(primary_key=True, max_length=2)
