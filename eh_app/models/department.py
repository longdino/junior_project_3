from . import _BaseTimestampModel
from django.db import models

class Department(_BaseTimestampModel):
    class Meta:
        db_table = 'department'

    name = models.CharField(max_length=7, primary_key=True)
