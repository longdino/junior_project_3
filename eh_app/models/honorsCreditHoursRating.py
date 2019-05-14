from . import _BaseTimestampModel
from ..querysets import HonorsCreditHoursRatingQueryset
from django.db import models

class HonorsCreditHoursRating(_BaseTimestampModel):
    class Meta:
        db_table = 'honors_credit_hours_rating'

    # id autogen
    hours_needed_per_sem = models.FloatField(unique=True)
    rating = models.CharField(max_length=16)

    objects = HonorsCreditHoursRatingQueryset.as_manager()
