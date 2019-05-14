from . import _BaseTimestampModel
from django.db import models

class ActivityAdvisingException(_BaseTimestampModel):
    class Meta:
        db_table = 'activity_advising_exception'
        unique_together = (('exception', 'department'),)

    advising_per_sem = models.FloatField(default=0)
    activities_per_sem = models.FloatField(default=0)

    # Relations
    exception = models.ForeignKey('Exception', related_name='activity_exception_set', on_delete=None)
    department = models.ForeignKey('Department', related_name='activity_exception_set', on_delete=None)

    def activities_per_year(self): # pragma: no cover
        return self.activities_per_sem * 2

    def advising_per_year(self): # pragma: no cover
        return self.advising_per_sem * 2
