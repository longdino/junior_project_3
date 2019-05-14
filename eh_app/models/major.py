from . import _BaseTimestampModel
from django.db import models

class Major(_BaseTimestampModel):
    class Meta:
        db_table = 'major'
        unique_together = (('track', 'concentration'),)

    name = models.CharField(max_length=4, primary_key=True)
    concentration = models.CharField(max_length=16, default=None, null=True)

    # Relations
    track = models.ForeignKey('Track', on_delete=None)
    department = models.ForeignKey('Department', on_delete=None)
