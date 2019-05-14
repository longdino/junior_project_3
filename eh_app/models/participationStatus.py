from . import _BaseTimestampModel
from ..querysets import ParticipationStatusQueryset
from django.db import models

class ParticipationStatus(_BaseTimestampModel):
    class Meta:
        db_table = 'participation_status'
        unique_together = (('honors_credit_rating', 'activity_requirement_rating', 'annual_report_rating', 'advising_requirement_rating', 'status'),)

    # id autogen
    season = models.CharField(max_length=16)
    honors_credit_rating = models.CharField(max_length=16)
    activity_requirement_rating  = models.CharField(max_length=16)
    annual_report_rating = models.CharField(max_length=16)
    advising_requirement_rating = models.CharField(max_length=16)
    status = models.CharField(max_length=45)

    objects = ParticipationStatusQueryset.as_manager()
