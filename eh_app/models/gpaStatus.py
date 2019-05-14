from . import _BaseTimestampModel
from ..querysets import GPAStatusQueryset
from django.db import models

class GPAStatus(_BaseTimestampModel):
    class Meta:
        db_table = 'gpa_status'
        unique_together = (('code', 'max_gpa'),)

    # id autogen
    code = models.CharField(max_length=2)
    max_gpa = models.DecimalField(max_digits=3, decimal_places=2)
    status = models.CharField(max_length=45)

    objects = GPAStatusQueryset.as_manager()
