from . import _BaseTimestampModel
from django.db import models

# Essentially a history element
class StudentResearch(_BaseTimestampModel):
    class Meta:
        db_table = 'student_research'

    # id autogen
    course_credit = models.PositiveIntegerField(default=None, null=True)
    paper_published = models.CharField(max_length=2, default=None, null=True)
    conference_attended = models.CharField(max_length=2, default=None, null=True)
    presentation = models.CharField(max_length=2, default=None, null=True)
    details = models.TextField(max_length=255, default=None, null=True)

    # Relations
    student = models.ForeignKey('Student', on_delete=None)
    research = models.ForeignKey('Research', on_delete=None)
    semester = models.ForeignKey(
        'Semester',
        default=None,
        null=True,
        on_delete=None,
    )
    # requirement can be reached through research.requirement
