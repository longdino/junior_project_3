from . import _BaseTimestampModel
from django.db import models

class Track(_BaseTimestampModel):
    class Meta:
        db_table = 'track'

    code = models.PositiveIntegerField(primary_key=True)
    id = models.CharField(max_length=15)
    name = models.CharField(max_length=45)

    # Relations
    semester_started = models.ForeignKey('Semester', on_delete=None, null=True)
    requirements = models.ForeignKey('TrackRequirements', on_delete=None)
    department = models.OneToOneField('Department', on_delete=None)
    college = models.ForeignKey('College', on_delete=None)

    def activities_per_sem(self): # pragma: no cover
        return self.requirements.activities_per_sem

    def advising_per_sem(self): # pragma: no cover
        return self.requirements.advising_per_sem

    def activities_per_year(self): # pragma: no cover
        return self.requirements.activities_per_year()

    def advising_per_year(self): # pragma: no cover
        return self.requirements.advising_per_year()

    def hours_required(self):
        return self.requirements.eh_hours
