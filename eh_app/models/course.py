from . import _BaseTimestampModel
from django.db import models

class Course(_BaseTimestampModel):
    class Meta:
        db_table = 'course'
        unique_together = (('number', 'department'),)

    # id autogen pk
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=45, default=None, null=True)
    credits = models.PositiveIntegerField()
    min_credits = models.PositiveIntegerField(default=None, null=True)
    max_credits = models.PositiveIntegerField(default=None, null=True)

    # Relations
    department = models.ForeignKey('Department', on_delete=None)
