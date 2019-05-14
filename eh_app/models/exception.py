from . import _BaseTimestampModel
from django.db import models

class Exception(_BaseTimestampModel):
    class Meta:
        db_table = 'exception'

    name = models.CharField(primary_key=True, max_length=45)
