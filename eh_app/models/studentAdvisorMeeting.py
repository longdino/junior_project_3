from . import _BaseTimestampModel
from django.db import models

# Essentially a history element
class StudentAdvisorMeeting(_BaseTimestampModel):
    class Meta:
        db_table = 'student_advisor_meeting'
        unique_together = (('date', 'student', 'advisor', 'semester'),)

    # id autogen
    date = models.CharField(max_length=10, default=None, null=True)
    details = models.TextField(max_length=255, default=None, null=True)

    # Relations
    student = models.ForeignKey('Student', on_delete=None)
    advisor = models.ForeignKey('Advisor', default=None, null=True, on_delete=None)
    semester = models.ForeignKey('Semester', on_delete=None)
