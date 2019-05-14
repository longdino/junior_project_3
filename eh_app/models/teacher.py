from . import _BaseTimestampModel
from django.db import models

class Teacher(_BaseTimestampModel):
    class Meta:
        db_table = 'teacher'

    uin = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max_length=45, default=None, null=True)
    last_name = models.CharField(max_length=45, default=None, null=True)
    middle_name = models.CharField(max_length=45, default=None, null=True)
