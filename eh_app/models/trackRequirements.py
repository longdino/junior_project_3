from . import _BaseTimestampModel, Requirement
from django.db import models

class TrackRequirements(_BaseTimestampModel):
    class Meta:
        db_table = 'track_requirement'

    # id autogen
    advising_per_sem = models.DecimalField(max_digits=2, decimal_places=1)
    activities_per_sem = models.DecimalField(max_digits=2, decimal_places=1)
    description = models.TextField(max_length=255, default=None, null=True)

    eh_hours = models.PositiveIntegerField(default=0)
    # senior_honors_thesis = models.TextField(default=None, null=True) - moved to Student as bool

    # research_credits = models.PositiveIntegerField(default=0) - moved to Student as bool
    # Relations
    requirements = models.ManyToManyField('Requirement', related_name='track_requirements_set')

    def activities_per_year(self): # pragma: no cover
        return self.activities_per_sem * 2

    def advising_per_year(self): # pragma: no cover
        return self.advising_per_sem * 2

    def activities_overall(self): # pragma: no cover
        return self.activities_per_year() * 4

    def add_requirement(self, req_code):
        elems = Requirement.objects.filter(code=req_code)

        if len(elems):
            return elems.last()
        else:
            return None

    def advising_overall(self): # pragma: no cover
        return self.advising_per_year() * 4
