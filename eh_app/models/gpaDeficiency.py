from . import _BaseTimestampModel
from django.db import models

class GPADeficiency(_BaseTimestampModel):
    class Meta:
        db_table = 'gpa_deficiency'

    value = models.CharField(primary_key=True, max_length=45)
    code = models.CharField(max_length=2)
