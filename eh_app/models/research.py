from . import _BaseTimestampModel
from django.db import models

class Research(_BaseTimestampModel):
    class Meta:
        db_table = 'research'

    # id autogen
    program = models.CharField(max_length=50, default=None, null=True)
    details = models.TextField(max_length=255, default=None, null=True)

    # Relations
    requirement_satisfied = models.ForeignKey('Requirement', default=None, null=True, on_delete=None)
    advisor = models.ForeignKey('Advisor', default=None, null=True, on_delete=None)
    track = models.ForeignKey('Track', on_delete=None)
