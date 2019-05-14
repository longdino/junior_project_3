from . import _BaseTimestampModel
from ..querysets import ProbAndGPADefQueryset
from django.db import models

class ProbDefStatus(_BaseTimestampModel):
    class Meta:
        db_table = 'prob_def_status'
        unique_together = (('gpa_status', 'max_gpa'),)

    #id autogen
    gpa_status = models.CharField(max_length=40)
    max_gpa = models.CharField(max_length=30)
    status = models.CharField(max_length=62)

    objects = ProbAndGPADefQueryset.as_manager()
