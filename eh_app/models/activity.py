from . import _BaseTimestampModel
from django.db import models

class Activity(_BaseTimestampModel):
    class Meta:
        db_table = 'activity'
        unique_together = (('date', 'location', 'semester'),)

    # id autogenerated
    date = models.CharField(max_length=10, default=None, null=True)
    location = models.CharField(max_length=45, default=None, null=True)
    details = models.TextField(max_length=255, default=None, null=True)

    # Relations
    semester = models.ForeignKey('Semester', on_delete=None)
