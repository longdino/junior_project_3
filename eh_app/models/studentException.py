from . import _BaseTimestampModel
from django.db import models

class StudentException(_BaseTimestampModel):
    class Meta:
        db_table = 'student_exception'
        unique_together = (('student', 'applicable_semester'),)

    #id autogen
    type_of_leave = models.CharField(max_length=45, default=None, null=True)
    leave_duration = models.CharField(max_length=10, default=None, null=True)

    # Relations
    applicable_semester = models.ForeignKey('Semester', related_name='student_exception_set', on_delete=None) # Starting semester
    student = models.ForeignKey(
        'Student',
        on_delete=None,
    )
    exception_rules = models.ForeignKey('ActivityAdvisingException', related_name='student_exception_set', on_delete=None)

    # Following covered by django tests
    def activities_per_sem(self): # pragma: no cover
        return self.exception_rules.activities_per_sem

    def advising_per_sem(self): # pragma: no cover
        return self.exception_rules.advising_per_sem

    def activities_per_year(self): # pragma: no cover
        return self.activities_per_sem() * 2

    def advising_per_year(self): # pragma: no cover
        return self.advising_per_sem() * 2

    def concat_uin_sem(self):
        return "{}{}".format(
            self.student.uin,
            self.applicable_semester.id
        )
