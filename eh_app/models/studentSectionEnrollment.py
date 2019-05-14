from . import _BaseTimestampModel
from ..querysets import StudentSectionEnrollmentQueryset
from django.db import models

# Essentially a history element
class StudentSectionEnrollment(_BaseTimestampModel):
    class Meta:
        db_table = 'student_section_enrollment'
        unique_together = (('section', 'student'),)

    # id autogen
    grade = models.CharField(max_length=2, default=None, null=True) # A,B,C,D,F,F*,I,NG,Q,X,W
    grading_mode = models.CharField(max_length=10, default=None, null=True) # S/U   FIXME: Does a non-passing D become U?
    repeat = models.CharField(max_length=10, default=None, null=True)

    # Relations
    section = models.ForeignKey('Section', related_name='section_enrollment_set', on_delete=None)
    student = models.ForeignKey('Student', related_name='enrolled_section_set', on_delete=None)

    objects = StudentSectionEnrollmentQueryset.as_manager()

    def semester(self): # pragma: no cover
        return self.section.semester

    def credits(self): # pragma: no cover
        return self.section.credits()

    def is_eh(self): # pragma: no cover
        return self.section.eh

    # Is enrollment filled out?
    # Must be valid on semester change
    def valid(self): # pragma: no cover
        return self.grade or self.grading_mode
