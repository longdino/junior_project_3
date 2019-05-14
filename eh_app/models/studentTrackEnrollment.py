from . import _BaseTimestampModel
from django.db import models

# Essentially a history element
class StudentTrackEnrollment(_BaseTimestampModel):
    class Meta:
        db_table = 'student_track_enrollment'

    # id autogen

    # Relations
    student = models.ForeignKey('Student', related_name='track_enrollment', default=None, on_delete=None)
    track = models.ForeignKey('Track', on_delete=None)
    semester = models.ForeignKey('Semester', on_delete=None)
    campus = models.ForeignKey('Campus', default=None, null=True, on_delete=None)
