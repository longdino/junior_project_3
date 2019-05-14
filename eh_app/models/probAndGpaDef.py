from . import _BaseTimestampModel
from django.db import models

class ProbAndGPADef(_BaseTimestampModel):
    class Meta:
        db_table = 'probation_and_gpa_def'
        unique_together = (('gpa_status', 'max_current_gpa'),)

    #id autogen
    gpa_status = models.CharField(max_length=40)
    max_current_gpa = models.CharField(max_length=30)
    status = models.CharField(max_length=62)
